"""[Docstring] Declares trucks' service class."""
# Imports
from . import models
import validation
# Trucks' service class.
class service:
    """[Docstring] Declares functions altering trucks' properties.
    
    Functions: changeTruckIdentificator(truckId, newTruckId), changeConvoyPosition(truckId, newConvoyPosition),
               changeConvoyLeader(truckId, newConvoyLeaderId), changeSpeed(truckId, speedOffset)
    """

    # Function changing truck identificator.
    def changeTruckIdentificator(truckId, newTruckId):
        """[Docstring] Change identificator of a truck.
        
        Inputs: Integer truckId, Integer newTruckId.
        """
        # Id validation: If truck's old and new id are integers, set new id and signal success.
        if validation.validate_int(truckId) and validation.validate_int(newTruckId):
            # Set new id on truck object referenced by the old id.
            models.Truck.objects.get(truckId=truckId).truckId = newTruckId
            # Signal success, via returning true.
            return True
        # If validation went wrong, signal failure.
        else: 
            # Signal failure, via returning false.
            return False
    
    # Function changing truck's position in convoy reference.
    def changeConvoyPosition(truckId, newConvoyPosition):
        """[Docstring] Change convoy position reference of a truck.
        
        Inputs: Integer truckId, Integer newConvoyPosition.
        """
        # Position validation: If truck's id and new position are integers (unnecessary: and the truck's new position is not the old one), set new position in convoy.
        if validation.validate_int(truckId) and validation.validate_int(newConvoyPosition):
            # Set new position on truck object referenced by its' truck id.
            models.Truck.objects.get(truckId=truckId).convoyPosition = newConvoyPosition
            # Signal success, via returning true.
            return True
        # If validation went wrong, signal failure.
        else: 
            # Signal failure, via returning false.
            return False

    # Function changing truck's convoy leader reference.
    def changeConvoyLeader(truckId, newConvoyLeaderId):
        """[Docstring] Change convoy's leader reference of a truck.
        
        Inputs: Integer truckId, Integer newConvoyLeaderId.
        """
        # Leader validation: If truck's id and the new convoy leader's id are integers, set new leaders position.
        if validation.validate_int(truckId) and validation.validate_int(newConvoyLeaderId):
            # Set new convoy leader's id on truck object referenced by its' truck id.
            models.Truck.objects.get(truckId=truckId).convoyLeaderId = newConvoyLeaderId
        # Signal success, via returning true.
            return True
        # If validation went wrong, signal failure.
        else: 
            # Signal failure, via returning false.
            return False

    # Function evaluating speed change and setting speed of a truck.
    def changeSpeed(truckId, speedOffset):
        """[Docstring] Change driving speed of a truck.
        
        Inputs: Integer truckId, Integer speedOffset.
        """
        # Speed validation: If truck's id is an integer, the speed offset is a float, set truck's speed, according to its' max speed and signal success.
        if validation.validate_int(truckId) and validation.validate_float(speedOffset):
            # Set truck's speed, according to its' max speed, referenced by its' id.
            # bind new speed and max speed of the truck for performance reasons
            newSpeed = float(speedOffset + models.Truck.objects.get(truckId = truckId).speed)
            maxSpeed = float(models.Truck.objects.get(truckId = truckId).maxSpeed)
            # If new speed is inbetween 0 and max speed, set new speed.
            if newSpeed < maxSpeed and newSpeed >= 0:
                # Set new speed on truck object referenced by its' id.
                models.Truck.objects.get(truckId = truckId).speed += speedOffset
            # If new speed is lower 0, set 0 as new speed.
            elif newSpeed < 0:
                # Set new speed on truck object accordingly, referenced by its' id
                models.Truck.objects.get(truckId = truckId).speed = 0
            # If new speed is above truck's max speed, set max speed as new speed
            elif newSpeed > maxSpeed:
                # Set new speed on truck object accordingly, referenced by its' id
                models.Truck.objects.get(truckId = truckId).speed = maxSpeed
            # Signal success, via returning true.
            return True
        # If validation went wrong, signal failure.
        else: 
            # Signal failure, via returning false.
            return False
