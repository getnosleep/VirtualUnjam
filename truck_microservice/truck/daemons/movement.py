# library imports
from threading import Thread
import time

# property imports
from ..properties import ID, DEPARTURE_DISTANCE

# persistence layer imports
from ..models import TruckEntity

class Movement(Thread):
    def __init__(self):
        Thread.__init__(self, daemon=True)
        self.accelerationTime = None
    
    def run(self):
        while True:
            # if heartbeat%2 == 0: => alle 40ms
            delay = .05
            time.sleep(delay)
            self.calculateSpeed(delay*1000)
            # Here has to be the subscriber/listener
            pass

    def setAccelerationTime(self, flank):
        self.accelerationTime = flank

    def __leaveConvoyFlank__(self, position, currentDistance, maxDistance):
        departure = maxDistance - DEPARTURE_DISTANCE
        return currentDistance > departure and position

    def __linearVelocity__(self, s_0, v_0, t):
        # s = v(0) t + s(0) -> distance calculation for linear velocities
        s = v_0 * t + s_0
        return s

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

            return [s, v_1, True]

        # inside speed limitation
        else:
            # s = 1/2 a t² + v(0) t + s(0) -> distance calculation for linear accelerating velocities
            s = 0.5 * a * t**2 + v_0 * t + s_0
        
            return [s, v, False]

    def calculateSpeed(self, t_ms):
        # placeholder
        targetVelocity = False
        s = .0
        v = .0

        # setup data
        t = t_ms*1.0 / 1000.0
        truck = TruckEntity.objects.get(pk=ID)
        s_0, v_0, a = truck.movementStats()
        s_1, v_1 = truck.targetStats()

        if not a and v_0 == v_1:
            v = v_0
            s = self.__linearVelocity__(s_0, v_0, t)
        else:
            s, v, targetVelocity = self.__acceleratingVelocity__(s_0, v_0, v_1, a, t)
        
        print(f'Position: {truck.position}\tSpeed: {v * 3.6}\tDistance: {s}')

        if not s or not v:
            # standing still
            return False

        if self.__leaveConvoyFlank__(truck.position, s, s_1):
            TruckEntity.objects.filter(address=truck.frontTruckAddress).delete()
            truck.leadingTruckAddress = None
            truck.frontTruckAddress = None
            truck.backTruckAddress = None
            truck.position = None
            truck.polling = False
        
        truck.currentRouteSection = s
        truck.currentSpeed = v

        if targetVelocity:
            truck.targetSpeed = v
            truck.acceleration = .0

        truck.save()

        return True
