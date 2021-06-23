# library imports
from threading import Thread
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from django.http import HttpResponse

# functional imports
from .daemons.bully import finishBullying, bully

# property imports
from .properties import ID

# persistence layer imports
from .models import TruckEntity

# extern requests
from .extern_api.addresses import join
from .extern_api.trucks import convoyRequest, joinBehind

# exception imports
from django.core.exceptions import ValidationError
from .exceptions.invalid_input import AccelerationException, NoMemberException, TruckBrokenException

# dirty imports => needed to start the subscriber daemon of a truck ... just trust me :)
from .daemons.subscriber import subscription

class Mutation(viewsets.ViewSet):
# CONVOY
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

                if truckInFront:
                    informTruckInFront = joinBehind(truckInFront)

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

    def joinBehind(self, request):
        try:
            truck = TruckEntity.objects.get(pk=ID)
            if truck.position:
                data = JSONParser().parse(request)
                newTruckBehind = data['backTruckAddress']
                truck.backTruckAddress = newTruckBehind
                truck.save()
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=500)

    def leaveConvoy(self, request):
        try:
            truck = TruckEntity.objects.get(pk=ID)
            truck.position = None
            truck.leadingTruckAddress = None
            truck.frontTruckAddress = None
            truck.backTruckAddress = None
            truck.polling = False
            truck.closing = False

            # Maybe unwanted, but nice to see => a leaving truck has to stop :D
            truck.targetSpeed = .0
            truck.acceleration = -1.0
            
            truck.full_clean()
            truck.save()
            return HttpResponse(status=200)
        except ValidationError as e:
            return HttpResponse('Database inconsistency found.', status=401)
        except Exception as e:
            return HttpResponse('Leaving not possible.', status=500)


# INTACT
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


# ACCELERATE
    def accelerate(self, request):
        try:
            truck = TruckEntity.objects.get(pk=ID)
            if truck.broken:
                raise TruckBrokenException()

            data = JSONParser().parse(request)
            if not truck.position or truck.leadingTruckAddress == truck.address or truck.leadingTruckAddress == data['self']:
                acc = data['acceleration']
                vel = data['targetSpeed'] / 3.6 # m/s to km/h

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


# BULLY
    def startBullying(self, request):
        try:
            truck = TruckEntity.objects.get(pk=ID)
            if truck.position:
                data = JSONParser().parse(request)
                newTruckBehind = data['backTruckAddress']
                truck.backTruckAddress = newTruckBehind
                truck.polling = True
                truck.save()
                bully()
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=500)

    def updateAfterBullying(self, request):
        try:
            data = JSONParser().parse(request)
            newLeader = data['newLeader']
            newTruckInFront = data['frontTruckAddress']
            frontTruckPosition = data['frontTruckPosition']

            truck = TruckEntity.objects.get(pk=ID)
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

            # Thread -> otherwise it might be a dead end and all the requests in this streak will be declined
            close = Thread(finishBullying(truckBehind, newLeader, oldPosition, newPosition), daemon=True)
            close.start()
            return HttpResponse(status=200)
        except NoMemberException as e:
            return HttpResponse(e.message, status=404)
        except Exception as e:
            return HttpResponse(status=500)
