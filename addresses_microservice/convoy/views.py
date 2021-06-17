from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.parsers import JSONParser

class ConvoyViewSet(viewsets.ViewSet):
    # {ID: ADDRESS_SELF, . . . }
    registered = {}
    
    def register(self, request):
        """
            POST: Registrates the requesting truck

            @requestJson:
                {
                    "truckId": ID of the requesting truck
                    "address": ADDRESS_SELF of the requesting truck
                }
            
            @return successful registration: bool
        """
        try:
            data = JSONParser().parse(request)
            truckId = data['truckId']
            address = data['address']
            self.registered[truckId] = address

            # position = len(self.registered) + 1
            # self.registered[position] = address
            return HttpResponse(True, status=200)
        except:
            return HttpResponse(False, status=404)

    def data(self, request):
        """
            GET: List of adresses of the trucks in this convoy

            @returnJson:
                {
                    "registered": registered-dictionary above
                }
        """
        return JsonResponse(self.registered, status=200)
    
    def bully(self, request):
        """
            PUT: Bullies a truck if possible

            @requestJson:
                {
                    "bulliedtruckId": ID of the leaving truck
                    "bulliedtruckAddress": ADDRESS_SELF of the leaving truck
                }

            @return A string statement of the done action: str
        """
        try:
            data = JSONParser().parse(request)
            bulliedTruckId = data['bulliedTruckId']
            bulliedTruckAddress = data['bulliedTruckAddress']

            registeredValue = self.registered.get(bulliedTruckId)

            if registeredValue and registeredValue == bulliedTruckAddress:
                result = str('Truck %s got kicked', self.registered.pop(bulliedTruckId, '???'))
                return HttpResponse(result, status=200)
            else:
                return HttpResponse('Already kicked', status=200)
        except:
            return HttpResponse('Ya mad bro?', status=404)
        
    def flush(self, request):
        """
            DELETE: Flushes the registered trucks and addresses

            @requestJson:
                {
                    "parol": Password to do this -> you won't get it
                }

            @return An absolutely not necessary string: str 
        """
        try:
            data = JSONParser().parse(request)
            if data['parol'] == 'idi na chui':
                self.registered = {}
                return HttpResponse('Cleared', status=200)
            else:
                raise Exception()
        except Exception as e:
            return HttpResponse('Ne ne ne', status=404)
