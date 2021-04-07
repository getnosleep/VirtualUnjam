from .models import Truck
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
    def validateTruckObjectStructure(self, truckId: int, maxSpeed: float):
        """[Docstring] Validates structure of a truck object.
        
        Inputs:
        
            Integer truckId.
        
        Results:

            True - In case the truck's truckId reference could be set.

            False - In case the update validation went wrong.

            Exception - In case the input validation went wrong.

        Logic:

            1.  Validates Inputs.

            2.  Binds truck model object to variable referenced by its' truckId.

            3.  Validates truck model object's structure.

            3.1 Signals success on valid structure, via returning true.

            3.2 Signals failure on invalid structure, via returning false.
        """
        # Bind truck object to reference.
        truck = Truck.objects.get(truckId=truckId)
        # Validate object's structure and serve function call accordingly.
        return validate_structure(truck.values(), schema={
                                                          "id": validate_int(min_value = 0),
                                                          "truckId": validate_int(min_value = 0),
                                                          "convoyPosition": validate_int(min_value = 0),
                                                          "convoyLeaderId": validate_int(min_value = 0),
                                                          "maxSpeed": validate_float(min_value = 0),
                                                          "speed": validate_float(min_value = 0, max_value = maxSpeed)
                                                        })

    # Function validating truck object's convoy leadership.
    def validateConvoyLeadership(self, truckId: int):
        """[Docstring] Validates convoy leadership of a truck object.
        
        Inputs:
        
            Integer truckId.
        
        Results:

            True - In case the truck object is its' convoy's leader.

            False - In case the update validation went wrong.

            Exception - In case the input validation went wrong.

        Logic:

            1.  Validates Inputs.

            2.  Binds truck model object to variable referenced by its' truckId.

            3.  Validates equality of truck's id and convoy leader's id.

            3.1 Signals success on valid update, via returning true.

            3.2 Signals failure on invalid update, via returning false.
        """
        # Bind truck object to reference.
        truck = Truck.objects.get(truckId=truckId)
        # Validate if truck is the leader of its' convoy and serve function call accordingly.
        return truck.truckId == truck.convoyLeaderId
       

    # Function changing truck identificator.
    def changeTruckIdentificator(self, truckId: int, newTruckId: int):
        """[Docstring] Changes identificator of a truck.
        
        Inputs:
        
            Integer truckId, Integer newTruckId.
        
        Results:

            True - In case the truck's truckId reference could be set.

            False - In case the update validation went wrong.

            Exception - In case the input validation went wrong.

        Logic:

            1.  Validates Inputs.

            2.  Binds truck model object to variable referenced by its' truckId.

            3.  Sets new truck id input as truck's respective reference.

            4.  Validates value update.

            4.1 Signals success on valid update, via returning true.

            4.2 Signals failure on invalid update, via returning false.
        """
        # Bind truck object to reference.
        truck = Truck.objects.get(truckId=truckId)
        # Set new truckId as truck's respective reference.
        truck.truckId.set(newTruckId) 
        # Save the truck and bind it to a reference.
        val = truck.save(force_insert = True)
        # Validate update via bound truck object and input.
        return val.truckId == newTruckId
    
    # Function changing truck's position in convoy reference.
    def changeConvoyPosition(self, truckId: int, newConvoyPosition: int):
        """[Docstring] Changes convoy position reference of a truck.
        
        Inputs: 
        
            Integer truckId, Integer newConvoyPosition.

        Results:

            True - In case the truck's convoyPosition reference could be set.

            False - In case the update validation went wrong.

            Exception - In case the input validation went wrong.

        Logic:

            1.  Validates Inputs.

            2.  Binds truck model object to variable referenced by its' truckId.

            3.  Sets new convoy leader's id input as truck's respective reference.

            4.  Validates value update.

            4.1 Signals success on valid update, via returning true.

            4.2 Signals failure on invalid update, via returning false.
        """
        # Bind truck object to reference
        truck = Truck.objects.get(truckId=truckId)
        # Set new convoy position as truck's respective reference.
        truck.convoyPosition.set(newConvoyPosition) 
        # Save the truck and bind it to a reference.
        val = truck.save(force_insert = True)
        # Validate update via bound truck object and input.
        return val.convoyPosition == newConvoyPosition

    # Function changing truck's convoy leader reference.
    def changeConvoyLeader(self, truckId: int, newConvoyLeaderId: int):
        """[Docstring] Change convoy's leader reference of a truck.
        
        Inputs: 
        
            Integer truckId, Integer newConvoyLeaderId.

        Results:

            True - In case the truck's convoyLeaderId reference could be set.

            False - In case the update validation went wrong.

            Exception - In case the input validation went wrong.

        Logic:

            1.  Validates Inputs.

            2.  Binds truck model object to variable referenced by its' truckId.

            3.  Sets new convoy leader's id input as truck's respective reference.

            4.  Validates value update.

            4.1 Signals success on valid update, via returning true.

            4.2 Signals failure on invalid update, via returning false.
        """
        # Bind truck object to reference
        truck = Truck.objects.get(truckId=truckId)
        # Set new convoy leader's id as truck's respective reference.
        truck.convoyLeaderId.set(newConvoyLeaderId)
        # Save the truck and bind it to a reference.
        val = truck.save(force_insert = True)
        # Validate update via bound truck object and input.
        return val.convoyPosition == newConvoyLeaderId
    
    # Function stopping truck.
    def stopTruck(self, truckId: int, newConvoyLeaderId: int):
        """[Docstring] Stopps truck entirely.
        
        Inputs: 
        
            Integer truckId, Integer newConvoyLeaderId.

        Results:

            True - In case the truck's convoyLeaderId reference could be set.

            False - In case the update validation went wrong.

            Exception - In case the input validation went wrong.

        Logic:

            1.  Validates Inputs.

            2.  Binds truck model object to variable referenced by its' truckId.

            3.  Sets truck's speed to 0.

            4.  Validates value update.

            4.1 Signals success on valid update, via returning true.

            4.2 Signals failure on invalid update, via returning false.
        """
        # Bind truck object to reference.
        truck = Truck.objects.get(truckId=truckId)
        # Set new convoy leader's id as truck's respective reference.
        truck.speed.set(0)
        # Save the truck and bind it to a reference.
        val = truck.save(force_insert = True)
        # Validate update via bound truck object and input.
        return val.speed == 0

    # Function evaluating speed change and setting speed of a truck.
    def changeSpeed(self, truckId: int, speedOffset: float, maxSpeed: float):
        """[Docstring] Changes driving speed of a truck.
        
        Inputs:

            Integer truckId, Float speedOffset.

        Results:

            True - In case the truck's new speed could be set.

            False - In case the update validation went wrong.

            Exception - In case the input validation went wrong.

        Logic:

            1.  Validates Inputs.

            2.  Binds truck model object to variable referenced by its' truckId.
        
            3.  Calculates truck's new speed.
        
            4.1 If new speed is inbetween 0 and maxSpeed input, keep new speed as speed to set

            4.2 If new speed is below 0, set 0 as new speed
        
            4.3 If the truck goes faster than its' terminal velocity, new speed will be set to that terminal velocity.

            5.  Saves evaluated new speed as truck's speed.

            6.  Validates value update.

            6.1 Signals success on valid update, via returning true.

            6.2 Signals failure on invalid update, via returning false.
        """
        # Bind truck object to reference.
        truck = Truck.objects.get(truckId=truckId)
        # Calculate truck's new speed.
        newSpeed = truck.speed + speedOffset
        # If truck's new speed is inbetween 0 and maxSpeed, set newSpeed as truck's speed.
        if newSpeed < maxSpeed and newSpeed >= 0:
            # keep new speed
            # newSpeed = newSpeed 
        # If new speed is lower 0, 0 will be as new speed.
        elif newSpeed < 0:
            # Bind new speed to reference for validation.
            newSpeed = 0
        # If new speed is above truck's max speed, max speed will be set as new speed.
        elif newSpeed > maxSpeed:
            # Set maxSpeed as newSpeed.
            newSpeed = maxSpeed
        # Set evaluated newSpeed as truck's speed.
        truck.speed.set(newSpeed)
        # Save the truck and bind it to a reference.
        val = truck.save(force_insert = True)
        # Validate update via bound truck object and input.
        return val.speed == newSpeed