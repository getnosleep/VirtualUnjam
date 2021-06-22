# library imports
from threading import Thread
from .daemons.bully import finishBullying, BullyAlgorithm, startBullyAlgorithm
from .exceptions.invalid_input import AccelerationException, NoMemberException, TruckBrokenException
from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
import concurrent.futures

# property imports
from .properties import ID

# persistence layer imports
from .models import TruckEntity

# dirty imports
from .daemons.subscriber import subscription

# extern requests
from .extern_api.addresses import join

# error messages
ERR_MSG_VALIDATION = 'Your input wasn\'t valid.'
ERR_MSG_ACCESSABILITY = 'Truck not accessible'

SUB = subscription

LEADER_POSITION = 1

class Mutation(viewsets.ViewSet):
    def joinConvoy(self, request):
        try:
            truck = TruckEntity.objects.get(pk=ID)
            if truck.broken:
                raise TruckBrokenException()

            response = join()
            if response and response.status_code == 200:
                data = response.json()
                position = data['position']
                truckInFront = data['truckInFront']
                truckBehind = data['truckBehind']
                truckLeader = data['truckLeader']

                if position and truckLeader:
                    truck = TruckEntity.objects.get(pk=ID)
                    truck.position = position
                    truck.frontTruckAddress = truckInFront
                    truck.backTruckAddress = truckBehind
                    truck.leadingTruckAddress = truckLeader
                    truck.full_clean()
                    truck.save()
                    return HttpResponse(status=200)
            elif response and response.status_code:
                return HttpResponse('Currently this truck can\'t join the convoy', status=400)
            else:
                return HttpResponse('The address microservice wasn\'t accessible.', status=400)
        except ValidationError as e:
            return HttpResponse('Database inconsistency found.', status=401)
        except TruckBrokenException as e:
            return HttpResponse(e.message, status=404)
        except Exception as e:
            return HttpResponse('Joining not possible.', status=500)

    def leaveConvoy(self, request):
        try:
            truck = TruckEntity.objects.get(pk=ID)
            truck.position = None
            truck.leadingTruckAddress = None
            truck.frontTruckAddress = None
            truck.backTruckAddress = None
            truck.polling = False
            truck.closing = False

            # Maybe unwanted, but nice to see
            truck.targetSpeed = .0
            truck.acceleration = -1.0
            
            truck.full_clean()
            truck.save()
            return HttpResponse(status=200)
        except ValidationError as e:
            return HttpResponse('Database inconsistency found.', status=401)
        except Exception as e:
            return HttpResponse('Leaving not possible.', status=500)

    def repair(self, request):
        try:
            truck = TruckEntity.objects.get(pk=ID)
            truck.broken = False
            truck.full_clean()
            truck.save()
            return HttpResponse(status=200)
        except ValidationError as e:
            return HttpResponse('Database inconsistency found.', status=401)
        except Exception as e:
            return HttpResponse('Repairing not possible.', status=500)
    
    def destroy(self, request):
        try:
            truck = TruckEntity.objects.get(pk=ID)
            truck.broken = True
            truck.full_clean()
            truck.save()
            return HttpResponse(status=200)
        except ValidationError as e:
            return HttpResponse('Database inconsistency found.', status=401)
        except Exception as e:
            return HttpResponse('Destroying not possible.', status=500)

    def accelerate(self, request):
        try:
            truck = TruckEntity.objects.get(pk=ID)
            if truck.broken:
                raise TruckBrokenException()

            if truck.leadingTruckAddress == truck.address or not truck.position:
                data = JSONParser().parse(request)
                
                acc = data['acceleration']
                vel = data['targetSpeed'] / 3.6

                if acc > .0 and vel > truck.currentSpeed or acc < .0 and vel < truck.currentSpeed:
                    truck.acceleration = acc
                    truck.targetSpeed = vel
                else:
                    raise AccelerationException()
                
                truck.full_clean()
                truck.save()

                return HttpResponse(status=200)
            else:
                raise AccelerationException('This truck isn\'t leader of the convoy, so it can\'t just randomly accelerate.')
        except TruckBrokenException as e:
            return HttpResponse(e.message, status=404)
        except ValidationError as e:
            return HttpResponse('Database inconsistency of invalid input.', status=401)
        except AccelerationException as e:
            return HttpResponse(e.message, status=404)
        except Exception as e:
            return HttpResponse('Acceleration settings are currently not possible.', status=500)

    def startBullying(self, request):
        try:
            truck = TruckEntity.objects.get(ID)
            if truck.position:
                data = JSONParser().parse(request)
                newTruckBehind = data['backTruckAddress']

                
                truck.backTruckAddress = newTruckBehind
                truck.polling = True
                truck.save()

                startBullyAlgorithm()

            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=500)

    def updateAfterBullying(self, request):
        try:
            data = JSONParser().parse(request)
            newLeader = data['newLeader']
            newTruckInFront = data['frontTruckAddress']
            frontTruckPosition = data['frontTruckPosition']

            truck = TruckEntity.objects.get(ID)
            truckBehind = truck.backTruckAddress
            oldPosition = truck.position
            newPosition = frontTruckPosition + 1

            if not oldPosition:
                raise NoMemberException()

            truck.leadingTruckAddress = newLeader
            truck.frontTruckAddress = newTruckInFront
            truck.position = newPosition
            truck.polling = False
            truck.save()

            # TODO eben checken ob der noch auf ne Variable verwiesen werden muss
            Thread(finishBullying(truckBehind, newLeader, oldPosition, newPosition), daemon=True)
            return HttpResponse(status=200)
        except NoMemberException as e:
            return HttpResponse(e.message, status=404)
        except Exception as e:
            return HttpResponse(status=500)
