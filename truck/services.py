from . import models
from validation import (
    validate_int, validate_float,
    validate_structure,
    validate_text,
)

class service:
    """[Docstring] Declares functions altering trucks' properties.
    
    Functions: 

        Names, inputs and results:

            validateTruckObjectStructure(truckId):boolean

            validateConvoyLeadership(truckId):boolean

            changeTruckIdentificator(truckId, newTruckId):boolean
            
            changeConvoyPosition(truckId, newConvoyPosition):boolean
            
            changeConvoyLeader(truckId, newConvoyLeaderId):boolean
            
            changeSpeed(truckId, speedOffset):boolean

        Hint: The respective docstrings hold a detailed behavioural description of the service class's functions.
    """

    # Function validating truck object's structure
    def validateTruckObjectStructure(self, truckId):
        """[Docstring] Validates structure of a truck object.
        
        Inputs:
        
            Integer truckId.
        
        Results:

            True - In case the truck's truckId reference could be set.

            False - In case the input validation went wrong.

        Logic:

            1. Checks if the truck object referenced by the truckId input, has a valid structure.

                1.1.0 Signals success, in case the truck object's structure is valid, the truck's truckId reference will be set according
                      to the newTruckId input.

                1.1.1 Signals failure, in case the truck object's structure is invalid.
        """        
        # Structure validation: If truckId is an integers and 
        # referenced truck object has the desired structure, function will signal success.
        if validate_int(truckId) and validate_structure(models.Truck.objects().get(truckId = truckId).values(), schema={"id": validate_int(min_value = 0), "truckId": validate_int(min_value = 0), "convoyPosition": validate_int(min_value = 0), "convoyLeaderId": validate_int(min_value = 0), "maxSpeed": validate_float(min_value = 0), "speed": validate_float(min_value = 0, max_value = models.Truck.objects().get(truckId = truckId).maxSpeed)}):
            # Signal success, via returning true.
            return True
        # If validation went wrong, function will signal failure.
        else: 
            # Signal failure, via returning false.
            return False

    # Function validating truck object's convoy leadership
    def validateConvoyLeadership(self, truckId):
        """[Docstring] Validates convoy leadership of a truck object.
        
        Inputs:
        
            Integer truckId.
        
        Results:

            True - In case the truck object is its' convoy's leader.

            False - In case the input validation went wrong.

        Logic:

            1. Checks if the truck object referenced by the truckId input, is leader of its' convoy.

                1.1.0 Signals success, in case the truck object's is validated as its' convoy's leader, the truck's truckId reference will
                      be set according to the newTruckId input.

                1.1.1 Signals failure, in case the truck object in not leader of its' convoy.
        """        
        # Structure validation: If truckId is an integers and 
        # referenced truck object has the desired structure, function will signal success.
        if validate_int(truckId) and models.Truck.objects.get(truckId = truckId).truckId == models.Truck.objects.get(truckId = truckId).convoyLeaderId:
            # Signal success, via returning true.
            return True
        # If validation went wrong, function will signal failure.
        else: 
            # Signal failure, via returning false.
            return False

    # Function changing truck identificator.
    def changeTruckIdentificator(self, truckId, newTruckId):
        """[Docstring] Changes identificator of a truck.
        
        Inputs:
        
            Integer truckId, Integer newTruckId.
        
        Results:

            True - In case the truck's truckId reference could be set.

            False - In case the input validation went wrong.

        Logic:

            1. Checks if truckId and newTruckId are integer.

                1.1.0 In case the inputs are valid, the truck's truckId reference will be set according to the newTruckId input.

                1.1.1 Signals success.
        
                1.2.0 Signals failure, in case inputs are invalid.
        """
        # Id validation: If truck's old and new id are integers, new id will be set and success signaled.
        if validate_int(truckId) and validate_int(newTruckId):
            # Set new id on truck object referenced by the old id.
            models.Truck.objects.get(truckId=truckId).truckId = newTruckId
            # Signal success, via returning true.
            return True
        # If validation went wrong, function will signal failure.
        else: 
            # Signal failure, via returning false.
            return False
    
    # Function changing truck's position in convoy reference.
    def changeConvoyPosition(self, truckId, newConvoyPosition):
        """[Docstring] Changes convoy position reference of a truck.
        
        Inputs: 
        
            Integer truckId, Integer newConvoyPosition.

        Results:

            True - In case the truck's convoyPosition reference could be set.

            False - In case the input validation went wrong.

        Logic:

            1. Checks if truckId and newConvoyPosition are integers.

                1.1.0 In case the inputs are valid, the truck's convoyLeaderId reference will be set according to the newConvoyLeaderId
                      input.

                1.1.1 Signals success.
        
                1.2.0 Will signal failure, in case inputs are invalid.
        """
        # Position validation: If truck's id and new position are integers (unnecessary: and the truck's new position is not the old one), function will set new position in convoy.
        if validate_int(truckId) and validate_int(newConvoyPosition):
            # Set new position on truck object referenced by its' truck id.
            models.Truck.objects.get(truckId=truckId).convoyPosition = newConvoyPosition
            # Signal success, via returning true.
            return True
        # If validation went wrong, function will signal failure.
        else: 
            # Signal failure, via returning false.
            return False

    # Function changing truck's convoy leader reference.
    def changeConvoyLeader(self, truckId, newConvoyLeaderId):
        """[Docstring] Change convoy's leader reference of a truck.
        
        Inputs: 
        
            Integer truckId, Integer newConvoyLeaderId.

        Results:

            True - In case the truck's convoyLeaderId reference could be set.

            False - In case the input validation went wrong.

        Logic:

            1. Checks if truckId is an integer and newConvoyLeaderId is an integer.

                1.1.0 In case the inputs are valid, the truck's convoyLeaderId reference will be set to the newConvoyLeaderId input
                      accordingly.

                1.1.1 Signals success.
        
                1.2.0 Will signal failure, in case inputs are invalid.
        """

        # Leader validation: If truck's id and the new convoy leader's id are integers, function will set new leader's id.
        if validate_int(truckId) and validate_int(newConvoyLeaderId):
            # Set new convoy leader's id on truck object referenced by its' truck id.
            models.Truck.objects.get(truckId=truckId).convoyLeaderId = newConvoyLeaderId
        # Signal success, via returning true.
            return True
        # If validation went wrong, function will signal failure.
        else: 
            # Signal failure, via returning false.
            return False

    # Function evaluating speed change and setting speed of a truck.
    def changeSpeed(self, truckId, speedOffset, maxSpeed):
        """[Docstring] Changes driving speed of a truck.
        
        Inputs:

            Integer truckId, Float speedOffset.

        Results:

            True - In case the truck's new speed could be set.

            False - In case the input validation went wrong.

        Logic:

            1. Checks if truckId is integer and speedOffset is float.

                1.1 In case the inputs are valid, evaluate the new speed the truck will reach.
        
                    2.1.0 If the truck reaches a negative velocity, its' speed will be set to 0.
        
                    2.1.1 Signals success.
        
                    2.2.0 If the truck goes faster than its' terminal velocity, the truck's speed will be set to that terminal velocity.

                    2.2.1 Signals success.
        
                    2.3.0 Does the truck not reach a negative velocity or does not go faster than it can, its' speed will be set to 
                          {speed = speedOffset + oldSpeed: 0 <= speed <= maxSpeed}.
        
                    2.3.1 Signals success.
        
                1.2 Will signal failure, in case inputs are invalid.
        """
        # Speed validation: If truck's id is an integer, the speed offset is a float, set truck's speed, according to its' max speed and signal success.
        if validate_int(truckId) and validate_float(speedOffset) and validate_float(maxSpeed):
            # Set truck's speed, according to its' max speed, referenced by its' id.
            # bind new speed of the truck for performance reasons
            newSpeed = float(speedOffset + models.Truck.objects.get(truckId = truckId).speed)
            # If new speed is inbetween 0 and max speed, set new speed.
            if newSpeed < maxSpeed and newSpeed >= 0:
                # Set new speed on truck object referenced by its' id.
                models.Truck.objects.get(truckId = truckId).speed = newSpeed
            # If new speed is lower 0, 0 will be as new speed.
            elif newSpeed < 0:
                # Set new speed on truck object accordingly, referenced by its' id
                models.Truck.objects.get(truckId = truckId).speed = 0
            # If new speed is above truck's max speed, max speed will be set as new speed
            elif newSpeed > maxSpeed:
                # Set new speed on truck object accordingly, referenced by its' id
                models.Truck.objects.get(truckId = truckId).speed = maxSpeed
            # Signal success, via returning true.
            return True
        # If validation went wrong, function will signal failure.
        else: 
            # Signal failure, via returning false.
            return False