from threading import Thread

from ..models import TruckEntity
from ..serializer import TruckSerializer
from ..exceptions.initialization import TruckNotInitializedException
from ..properties import TRUCK_ID, DEPARTURE_DISTANCE

class Movement(Thread):
    def __init__(self):
        self.is_alive = True
        self.run()
    
    def run(self):
        self.is_alive = True
        while self.is_alive:
            pass

    def stop(self):
        self.is_alive = False
        pass

    def __leaveConvoyFlank__(self, currentDistance, maxDistance):
        return abs(currentDistance + DEPARTURE_DISTANCE) > maxDistance

    def __linearVelocity__(self, s_0, v_0, t):
        # s = v(0) t + s(0) -> distance calculation for linear velocities
        s = v_0 * t + s_0
        return (s, v_0)

    def __acceleratingVelocity__(self, s_0, v_0, v_1, a, t):
        # v = a t + v(0) -> accelerating velocity
        v = a * t + v_0

        # If we get really curious about this, we should calculate the accelerating velocities by interpolation on a torque-curve
        # => no linear acceleration and a regulation for over- and undershooting that'd require complex numbers (++++ Oh man, I love 'control engineering' ++++)

        # prevent overacceleration/-deceleration
        if (a > 0.0 and v > v_1) or (a < 0.0 and v < v_1):
            t_a = (v_1 - v_0) / a

            # s = 1/2 a t(a)² + (v - v(0)) (t - t(a)) + v(0) t + s(0) -> distance calculation for linear accelerating velocities with absolute offset 
            s = 0.5 * a * t_a**2 + (v_1 - v_0) * (t - t_a) + v_0 * t + s_0

            return (s, v_1, True)

        # inside speed limitation
        else:
            # s = 1/2 a t² + v(0) t + s(0) -> distance calculation for linear accelerating velocities
            s = 0.5 * a * t**2 + v_0 * t + s_0
        
            return (s, v, False)

    def calculateSpeed(self, t_ms):
        # placeholder
        leave = False
        targetVelocity = False
        s = 0.0
        v = 0.0

        # setup data
        t = t_ms*1.0 / 1000.0
        truck = TruckEntity.objects.get(truckId=TRUCK_ID)
        s_0, v_0, a = truck.movementStats()
        s_1, v_1 = truck.targetStats()

        if self.__leaveConvoyFlank__(s_0, s_1):
            s = s_0
        elif a == 0.0 and v_0 == v_1:
            v = v_0
            s = self.__linearVelocity__(s_0, s_1, v_0, t)
        else:
            s, v, targetVelocity = self.__acceleratingVelocity__(s_0, s_1, v_0, v_1, a, t)
        
        if not s or not v:
            print('This is an Error that can\'t even exist, but yeah, okay... I\'m fine with this (crappy shit)')
            # truck.broken = True
            return False

        if leave or self.__leaveConvoyFlank__(s, s_1):
            truck.convoyLeader = 0
            truck.convoyPosition = 0
        
        truck.currentDistance = s
        truck.currentSpeed = v

        if targetVelocity:
            truck.targetSpeed = v
            truck.currentAcceleration = 0.0

        truck.save()

        return True

mover = Movement()
