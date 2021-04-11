import requests
from typing import Final
from rest_framework import status
from truck.models import Truck
from validation import (
    validate_int, validate_float,
    validate_structure,
    validate_text,
)

class Service(object):
    """[Docstring] Declares functions altering trucks' properties.
    
    Functions: 

        Names, inputs and results:

            validateTruckObjectStructure(truckId, maxSpeed):boolean

            validateLeadership(truckId):boolean

            changeTruckIdentificator(truckId, newTruckId):boolean
            
            changeConvoyPosition(truckId, newConvoyPosition):boolean
            
            changeConvoyLeader(truckId, newConvoyLeaderId):boolean
            
            changeSpeed(truckId, speedOffset):boolean
            
            determineTruckInFront(truckId):boolean to be edited
            
            determineTruckBehind(truckId):boolean to be edited

            adjustSpeedOfTruckToLeader(truckId):

            initiateVote(truckId):boolean

            pollingWithAnotherTruck(pollingTruckId):boolean

            pollingWithHigherIdentifiedTrucks(truckId, pollingTruckIds):boolean

        Hint: The respective docstrings hold a detailed behavioural description of the
              service class's functions.
    """

    # Static final references.
    maxSpeed:     Final[float] =  80.00
    truckAPIHost: Final[str]   = '127.0.0.1'
    truckAPIPort: Final[str]   = '8000'

    # Function validating truck object's structure.
    @staticmethod
    def validateTruckObjectStructure(truckId: int):
        """[Docstring] Validates structure of a truck object.
        
        Inputs:
        
            Integer truckId.
        
        Results:

            True        -   In case the truck's structure could be validated.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.
        
        Logic:

            1.  Validates Inputs.

            2.  Binds truck's model object to variable referenced by its' truckId.

            3.  Validates truck model object's structure.

            3.1 Signals success on valid structure, via returning true.

            3.2 Signals failure on invalid structure, via returning false.
        """
        # Bind truck's object to reference.
        truck = Truck.objects.get(truckId=truckId)
        # Validate object's structure and serve function call accordingly.
        return validate_structure(truck.values(), schema={
                                                          "id": validate_int(min_value = 0),
                                                          "truckId": validate_int(min_value = 0),
                                                          "convoyPosition": validate_int(min_value = 0),
                                                          "convoyLeaderId": validate_int(min_value = 0),
                                                          "speed": validate_float(min_value = 0, max_value = Service.maxSpeed)
                                                        })

    # Function validating truck object's convoy leadership.
    @staticmethod
    def validateConvoyLeadership(truckId: int):
        """[Docstring] Validates convoy leadership of a truck object.
        
        Inputs:
        
            Integer truckId.
        
        Results:

            True        -   In case the truck object is its' convoy's leader.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            1.  Validates Inputs.

            2.  Binds truck's model object to variable referenced by its' truckId.

            3.  Validates equality of truck's id and convoy leader's id.

            3.1 Signals success on valid update, via returning true.

            3.2 Signals failure on invalid update, via returning false.
        """
        # Bind truck's object to reference.
        truck = Truck.objects.get(truckId=truckId)
        # Validate if truck is the leader of its' convoy and serve function call accordingly.
        return truck.truckId == truck.convoyLeaderId
       

    # Function changing truck identificator.
    @staticmethod
    def changeTruckIdentificator(truckId: int, newTruckId: int):
        """[Docstring] Changes identificator of a truck.
        
        Inputs:
        
            Integer truckId, Integer newTruckId.
        
        Results:

            True        -   In case the truck's truckId reference could be set.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            1.  Validates Inputs.

            2.  Binds truck's model object to variable referenced by its' truckId.

            3.  Sets new truck id input as truck's respective reference.

            4.  Validates value update.

            4.1 Signals success on valid update, via returning true.

            4.2 Signals failure on invalid update, via returning false.
        """
        # Bind truck's object to reference.
        truck = Truck.objects.get(truckId=truckId)
        # Set new truckId as truck's respective reference.
        truck.truckId.set(newTruckId) 
        # Save the truck and bind it to a reference.
        val = truck.save(force_insert = True)
        # Validate update via bound truck object and input.
        return val.truckId == newTruckId
    
    # Function changing truck's position in convoy reference.
    @staticmethod
    def changeConvoyPosition(truckId: int, newConvoyPosition: int):
        """[Docstring] Changes convoy position reference of a truck.
        
        Inputs: 
        
            Integer truckId, Integer newConvoyPosition.

        Results:

            True        -   In case the truck's convoyPosition reference could be set.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            1.  Validates Inputs.

            2.  Binds truck's model object to variable referenced by its' truckId.

            3.  Sets new convoy leader's id input as truck's respective reference.

            4.  Validates value update.

            4.1 Signals success on valid update, via returning true.

            4.2 Signals failure on invalid update, via returning false.
        """
        # Bind truck object to reference.
        truck = Truck.objects.get(truckId=truckId)
        # Set new convoy position as truck's respective reference.
        truck.convoyPosition.set(newConvoyPosition)
        # Save the truck and bind.
        val = truck.save(force=True)
        # validate new position in convoy.
        return val.convoyPosition == newConvoyPosition

    # Function changing truck's convoy leader reference.
    @staticmethod
    def changeConvoyLeader(truckId: int, newConvoyLeaderId: int):
        """[Docstring] Change convoy's leader reference of a truck.
        
        Inputs: 
        
            Integer truckId, Integer newConvoyLeaderId.

        Results:

            True        -   In case the truck's convoyLeaderId reference could be set.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            1.  Validates Inputs.

            2.  Binds truck's model object to variable referenced by its' truckId.

            3.  Sets new convoy leader's id input as truck's respective reference.

            4.  Validates value update.

            4.1 Signals success on valid update, via returning true.

            4.2 Signals failure on invalid update, via returning false.
        """
        # Bind truck object to reference.
        truck = Truck.objects.get(truckId=truckId)
        # Set new convoy leader's id as truck's respective reference.
        truck.convoyLeaderId.set(newConvoyLeaderId)
        # Save the truck and bind it to a reference.
        val = truck.save(force_insert = True)
        # Validate update via bound truck object and input.
        return val.convoyLeaderId == newConvoyLeaderId
    
    # Function stopping truck.
    @staticmethod
    def stopTruck(truckId: int):
        """[Docstring] Stopps truck entirely.
        
        Inputs: 
        
            Integer truckId.

        Results:

            True        -   In case the truck's could be stopped.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            1.  Validates Inputs.

            2.  Binds truck's model object to variable referenced by its' truckId.

            3.  Sets truck's speed to 0.

            4.  Validates value update.

            4.1 Signals success on valid update, via returning true.

            4.2 Signals failure on invalid update, via returning false.
        """
        # Bind truck's object to reference.
        truck = Truck.objects.get(truckId=truckId)
        # Set new convoy leader's id as truck's respective reference.
        truck.speed.set(0)
        # Save the truck and bind it to a reference.
        val = truck.save(force_insert = True)
        # Validate update via bound truck object and input.
        return val.speed == 0

    # Function evaluating speed change and setting speed of a truck.
    @staticmethod
    def changeSpeed(truckId: int, speedOffset: float):
        """[Docstring] Changes driving speed of a truck.
        
        Inputs:

            Integer truckId, Float speedOffset.

        Results:

            True        -   In case the truck's new speed could be set.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            1.  Validates Inputs.

            2.  Binds truck's model object to variable referenced by its' truckId.
        
            3.  Calculates truck's new speed.
        
            4.1 If new speed is inbetween 0 and maxSpeed input, keep new speed as speed to set

            4.2 If new speed is below 0, set 0 as new speed
        
            4.3 If the truck goes faster than its' terminal velocity, new speed will be set to that terminal
                velocity.

            5.  Saves evaluated new speed as truck's speed.

            6.  Validates value update.

            6.1 Signals success on valid update, via returning true.

            6.2 Signals failure on invalid update, via returning false.
        """
        # Bind truck's object to reference.
        truck = Truck.objects.get(truckId=truckId)
        # Calculate truck's new speed.
        newSpeed = truck.speed + speedOffset
        # If truck's new speed is inbetween 0 and maxSpeed, set newSpeed as truck's speed.
        if validate_float(min_value=0, max_value=Service.maxSpeed,  value=newSpeed): pass
        # If new speed is lower 0, 0 will be as new speed.
        elif not validate_float(min_value = 0, value = newSpeed): newSpeed = 0
        # If new speed is above truck's max speed, max speed will be set as new speed.
        elif not validate_float(max_value=Service.maxSpeed, value=newSpeed): newSpeed = Service.maxSpeed
        # Set evaluated newSpeed as truck's speed.
        truck.speed.set(newSpeed)
        # Save the truck and bind it to a reference.
        val = truck.save(force_insert = True)
        # Validate update via bound truck object and input.
        return val.speed == newSpeed

    # Function adjust truck's speed to another truck.
    @staticmethod
    def adjustSpeedToTruck(truckId: int, idolTruckId: int):
        """[Docstring] Adjusts speed of the truck to another truck.

        Inputs:

            Integer truckId, Float speedOffset.

        Results:

            True        -   In case the truck's new speed could be set.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            1.  Validates Inputs.

            2.1 Binds truck's model object to variable referenced by its' truckId.

            2.2 Binds idol's model object to variable referenced by its' truckId.
                    
            3.  Sets truck's speed to idol's speed.

            4.  Validates value update.

            4.1 Signals success on valid update, via returning true.

            4.2 Signals failure on invalid update, via returning false.
        """
        # Bind truck's object to reference.
        truck = Truck.objects.get(truckId=truckId)
        # Bind idol truck's object to reference.
        idolTruck = Truck.objects.get(truckId=idolTruckId)
        # Adjust truck's speed to the idol's speed
        truck.speed.set(idolTruck.speed)
        # Save the truck and bind it to a reference.
        val = truck.save(force_insert=True)
        # Validate update via bound truck object and input.
        return val.speed == idolTruck.speed

    # Function polling two truck's via truckId reference
    @staticmethod
    def pollingWithAnotherTruck(truckId: int, pollingTruckId: int):
        """[Docstring] Polling in between truck and a another one.

        Inputs:

            Integer truckId, Integer pollingTruckId.

        Results:

            status.HTTP_404_NOT_FOUND  -   In case the referenced polling truck does not exist.
                
            status.HTTP_200_OK         -   In case the polling is successful.

            status.HTTP_403_FORBIDDEN  -   In case the polling is a failure.

            Exception                  -   In case the input validation went wrong.

        Logic:

            1.    Validates Inputs.

            2.    Binds polling truck's model object to variable referenced by its' truckId.
                    
            3.    Evaluate Polling.
                
            3.1.0 If the polling truck's truckId is bigger, it is not broken, will evaluate
                polling as lost.

            3.1.1 Signals null reference, via returning status.HTTP_404_NOT_FOUND.
                
            3.2.1 If the polling truck's truckId is bigger, but it's broken or truck is not in the convoy,
                  will evaluate polling as won.

            3.2.2 Signals success, via returning status.HTTP_200_OK.
                
            3.3.1 If it is not in existence, will evaluate polling as won.

            3.3.2 Signals failure, via returning status.HTTP_403_FORBIDDEN.
        """
        # Bind polling truck's model object and truck's model object, referenced by their truckId.
        val = Truck.objects.get(truckId=pollingTruckId)
        truck = Truck.objects.get(truckId=truckId)
        # Evaluate polling.
        if   not val:                                                                                          return status.HTTP_404_NOT_FOUND
        elif val.truckId <= truck.truckId and val.convoyleaderId == truck.convoyLeaderId:                      return status.HTTP_200_OK
        elif val.truckId >= truck.truckId and val.convoyleaderId == truck.convoyLeaderId and val.isBroken:     return status.HTTP_200_OK
        elif val.truckId >= truck.truckId and val.convoyleaderId == truck.convoyLeaderId and not val.isBroken: return status.HTTP_403_FORBIDDEN
        elif val.convoyleaderId != truck.convoyLeaderId:                                                       return status.HTTP_200_OK
    
    # Function polling two truck's via truckId reference.
    @staticmethod
    def pollingWithHigherIdentifiedTrucks(truckId: int, pollingTruckIds: list([int])):
        """[Docstring] Initiate vote among polling trucks.

        Inputs:

            Integer truckId, List pollingTruckIds.
            
        Results:

            True        -   In case the polling is successful.

            False       -   In case the polling is a failure.

            Exception   -   In case the input validation went wrong.

        Logic:

            1.    Validates Inputs.

            2.    Binds polling truck's model object to variable referenced by its' truckId.
                    
            3.    Iterate list of integers provided by the function call, via a for loop.
                
            3.1.0 Polls with respective truck, for each integer in provided list.

            3.1.1 If polling failed, stop truck from further polling.

            3.1.2 If polling is successful or truck is not in the convoy, will keep polling.

            3.1.3 If polling is succesful but the next truck isn't exisiting, will assume
                  convoy leadership.
                
            4.    Signals polling evaluation.

            4.1.0 Will signal success, if convoy leadership is optained.

            4.1.1 Will signal failure, if further polling is stopped.
        """
        # Bind truck's model object, referenced by its' their truckId.
        truck = Truck.objects.get(truckId=truckId)
        # Iterate list of integers provided by function call, polling with referenced trucks.
        for x in pollingTruckIds:
            # Bind polling result to reference for performance reason.
            result = Service.pollingWithAnotherTruck(truck.truckId, x)
            # Evaluate polling result.
            if   result == status.HTTP_404_NOT_FOUND: truck.convoyLeaderId.set(truck.truckId); truck.save(force=True)
            elif result == status.HTTP_200_OK:        pass
            elif result == status.HTTP_403_FORBIDDEN: break
        # Validate truck's convoy leadership.
        return Service.validateConvoyLeadership(truck.truckId)

    @staticmethod
    def initiateOneVote(toBullyTruckId: int, connectionAttempt: int, toBullyTruckIds:list([int])):
        try:
            # Increase connectionAttempt by one.
            connectionAttempt += 1
            # File post request for truck json against api.
            resp = requests.post(
                                'http://'
                                + Service.truckAPIHost + ':'
                                + Service.truckAPIPort + '/api/truck/'
                                + toBullyTruckId + '/vote/',
                                params=dict(
                                    higherIdentifiedTrucks=str(
                                        toBullyTruckIds
                                    )
                                )   
                            )
            # Will evaluate response status code to decide, if the truckId can be deleted from to-bully-truckIds-list
            # or has to be kept for further requests.
        except: pass
        finally: 
            if      resp.status_code == status.HTTP_200_OK: return True
            elif    connectionAttempt > 5:                  return False
            else:   Service.initiateOneVote(toBullyTruckId, connectionAttempt, toBullyTruckIds)
    
    @staticmethod
    def initiateAllVotes(truckId: int, convoyLeaderId: int, toBullyTruckIds: list([int])):
        for x in toBullyTruckIds: 
            if    Service.initiateOneVote(x, 0, toBullyTruckIds): toBullyTruckIds.remove(x)
            else:                                                 pass
        return toBullyTruckIds   

    @staticmethod
    def joinConvoy(truckId: int, convoyLeaderId: int):
        # Bind truck's model object, referenced by its' their truckId.
        truck = Truck.objects.get(truckId=truckId)
        # Set convoyLeaderId as truck's convoyLeaderId
        truck.convoyLeaderId.set(convoyLeaderId)
        # Save the truck and bind it to a reference.
        val = truck.save(force_insert=True)
        # Validate update via bound truck object and input.
        return val.convoyLeaderId == truck.convoyLeaderId

    
    @staticmethod
    def leaveConvoy(truckId: int):
        # Bind truck's model object, referenced by its' their truckId.
        truck = Truck.objects.get(truckId=truckId)
        # Set convoyLeaderId as truck's convoyLeaderId
        truck.convoyLeaderId.set(-1)
        # Save the truck and bind it to a reference.
        val = truck.save(force_insert=True)
        # Validate update via bound truck object and input.
        return val.convoyLeaderId == -1
