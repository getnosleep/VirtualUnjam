from django.db import models

# binding fields for serializers
__all__ = [ "id", "convoyLeaderId", "speed"]

class Convoy(object):
    """[Docstring] Declares model objects

    Properties:
    
        id Primary_key - UUID - Primary key for database,
        
        convoyLeaderId Integer - leader in distributed Convoy,
        
        speed Float - current target speed of the convoy.
    """

    id = models.AutoField(primary_key=True)
    #convoyId = models.IntegerField()
    convoyLeaderId = models.IntegerField()
    speed = models.FloatField()
