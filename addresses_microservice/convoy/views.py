from codecs import register
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.parsers import JSONParser

class ConvoyViewSet(viewsets.ViewSet):
    # {POSITION: ADDRESS_SELF}
    registered = {}
    def register(self, request):
        """
            POST: Registrates the requesting truck

            @requestJson:
                {
                    "truckId": ID of the requesting truck
                    "address": ADDRESS_SELF of the requesting truck
                }
            
            @return unsuccessful bool or position JSON
        """
        try:
            data = JSONParser().parse(request)
            address = data['address']
            if address:
                
                if address in self.registered.values():
                    keys = list(self.registered.keys())
                    values = list(self.registered.values())
                    position = keys[values.index(address)]
                else:
                    position = len(self.registered) + 1
                    self.registered[position] = address
                
                keys = list(self.registered.keys())
                values = list(self.registered.values())
                index = values.index(address)

                try:
                    print(values[index+1])
                    print(len(values))
                except:
                    pass

                truckInFront = values[index-1] if (index-1) >= 0 else None
                truckBehind = values[index+1] if (index+1) < len(values) else None
                truckLeader = values[0]

                data = {
                    'position': position,
                    'truckInFront': truckInFront,
                    'truckBehind': truckBehind,
                    'truckLeader': truckLeader
                }
                return JsonResponse(data, status=200)
            else:
                return HttpResponse(False, status=404)
        except:
            return HttpResponse(False, status=400)

    def data(self, request):
        """
            GET: List of adresses of the trucks in this convoy

            @returnJson:
                {
                    "registered": registered-dictionary above
                }
        """
        return JsonResponse(self.registered, status=200)
    
    def overwriteRegistration(self, request):
        """
            PUT: Overwrites the bullied position/truck

            @returnJson:
                {
                    "oldPosition": old position of the truck,
                    "newPosition": current position of the truck,
                    "address": trucks address,
                }
        """
        try:
            data = JSONParser().parse(request)
            oldPosition = data['oldPosition']
            newPosition = data['newPosition']
            truckAddress = data['address']

            if self.registered[oldPosition] == truckAddress and self.registered[newPosition] and oldPosition >= newPosition:
                self.registered.pop(oldPosition)
                self.registered[newPosition] = truckAddress
                return HttpResponse(status=200)
            else:
                return HttpResponse('You have no permission to do this', status=401)
        except:
            return HttpResponse('Possibly wrong input', status=400)
        
    def flush(self, request):
        """
            DELETE: Flushes the registered positioning of the truck addresses

            @requestJson:
                {
                    "parol": Password to do this -> you won't get it
                }

            @return An absolutely not necessary string: str 
        """
        try:
            data = JSONParser().parse(request)
            if data['parol'] == 'idi na chui':
                while len(self.registered):
                    key = next(iter(self.registered))
                    del self.registered[key]
                return HttpResponse(True, status=200)
        except Exception as e:
            pass
        return HttpResponse(False, status=400)
