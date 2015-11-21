"""
The huginn.aircraft module contains classes that wrap the jsbsim object and
return data about the simulation.
"""
from abc import ABCMeta, abstractmethod
import logging
from math import degrees

from PyJSBSim import tFull, FGTrim

from huginn.unit_conversions import (convert_feet_to_meters,
                                     convert_rankine_to_kelvin,
                                     convert_psf_to_pascal,
                                     convert_libra_to_newtons)

class Component(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update_from_fdmexec(self, fdmexec):
        pass

class GPS(Component):
    """The GPS class simulates the aircraft's GPS system."""
    def __init__(self):
        Component.__init__(self)

        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.airspeed = 0.0
        self.heading = 0.0

    def update_from_fdmexec(self, fdmexec):
        propagate = fdmexec.GetPropagate()

        self.latitude = propagate.GetLatitudeDeg()
        self.longitude = propagate.GetLongitudeDeg()

        self.altitude = propagate.GetAltitudeASLmeters()

        airspeed_in_fps = fdmexec.GetAuxiliary().GetVtrueFPS()
        self.airspeed = convert_feet_to_meters(airspeed_in_fps)
        #self.airspeed = convert_knots_to_meters_per_sec(airspeed_in_knots)

        self.heading = degrees(propagate.GetEuler().Entry(3))

class Accelerometer(Component):
    """The Accelerometer class returns the acceleration measures on the body
    frame."""
    def __init__(self):
        Component.__init__(self)

        self.x_acceleration = 0.0
        self.y_acceleration = 0.0
        self.z_acceleration = 0.0

    def update_from_fdmexec(self, fdmexec):
        auxiliary = fdmexec.GetAuxiliary()

        self.x_acceleration = convert_feet_to_meters(auxiliary.GetPilotAccel(1))

        self.y_acceleration = convert_feet_to_meters(auxiliary.GetPilotAccel(2))

        self.z_acceleration = convert_feet_to_meters(auxiliary.GetPilotAccel(3))

class Gyroscope(Component):
    """The Gyroscope class contains the angular velocities measured on the body axis."""
    def __init__(self):
        Component.__init__(self)

        self.roll_rate = 0.0
        self.pitch_rate = 0.0
        self.yaw_rate = 0.0

    def update_from_fdmexec(self, fdmexec):
        auxiliary = fdmexec.GetAuxiliary()
        
        self.roll_rate = degrees(auxiliary.GetEulerRates(1))

        self.pitch_rate = degrees(auxiliary.GetEulerRates(2))

        self.yaw_rate = degrees(auxiliary.GetEulerRates(3))

class Thermometer(Component):
    """The Thermometer class contains the temperature measured by the
    aircraft's sensors."""
    def __init__(self):
        Component.__init__(self)

        self.temperature = 0.0

    def update_from_fdmexec(self, fdmexec):
        #self.temperature = self.fdmexec.GetAuxiliary().GetTAT_C()
        self.temperature = convert_rankine_to_kelvin(fdmexec.GetAtmosphere().GetTemperature())

class PressureSensor(Component):
    """The PressureSensor class contains the static presured measured by the
    aircraft's sensors."""
    def __init__(self):
        Component.__init__(self)

        self.pressure = 0.0

    def update_from_fdmexec(self, fdmexec):
        self.pressure = convert_psf_to_pascal(fdmexec.GetAtmosphere().GetPressure())

class PitotTube(Component):
    """The PitosTure class simulates the aircraft's pitot system."""
    def __init__(self):
        Component.__init__(self)

        self.pressure = 0.0

    def update_from_fdmexec(self, fdmexec):
        self.pressure = convert_psf_to_pascal(fdmexec.GetAuxiliary().GetTotalPressure())

class InertialNavigationSystem(Component):
    """The InertialNavigationSystem class is used to simulate the aircraft's
    inertial navigation system."""
    def __init__(self):
        Component.__init__(self)

        self.roll = 0.0
        self.pitch = 0.0
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.airspeed = 0.0
        self.heading = 0.0

    def update_from_fdmexec(self, fdmexec):
        propagate = fdmexec.GetPropagate()

        euler_angles = propagate.GetEulerDeg()
        self.roll = euler_angles.Entry(1)

        self.pitch = euler_angles.Entry(2)

        self.heading = euler_angles.Entry(3)

        self.latitude = propagate.GetLatitudeDeg()
        self.longitude = propagate.GetLongitudeDeg()

        airspeed_in_fps = fdmexec.GetAuxiliary().GetVtrueFPS()
        self.airspeed = convert_feet_to_meters(airspeed_in_fps)

        self.altitude = propagate.GetAltitudeASLmeters()

class Controls(object):
    """The Controls class holds the aircraft control surfaces values"""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def aileron(self):
        """The aileron deflection."""
        return self.fdmexec.GetFCS().GetDaCmd()

    @aileron.setter
    def aileron(self, value):
        """Set the aileron deflection.

        This value must be between -1.0 and 1.0"""
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0

        self.fdmexec.GetFCS().SetDaCmd(value)

    @property
    def elevator(self):
        """The elevator deflection."""
        return self.fdmexec.GetFCS().GetDeCmd()

    @elevator.setter
    def elevator(self, value):
        """Set the elevator deflection.

        This value must be between -1.0 and 1.0"""
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0

        self.fdmexec.GetFCS().SetDeCmd(value)

    @property
    def rudder(self):
        """The rudder deflection."""
        return self.fdmexec.GetFCS().GetDrCmd()

    @rudder.setter
    def rudder(self, value):
        """Set the rudder deflection.

        This value must be between -1.0 and 1.0"""
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0

        self.fdmexec.GetFCS().SetDrCmd(value)

    @property
    def throttle(self):
        """The throttle setting."""
        return self.fdmexec.GetFCS().GetThrottleCmd(0)

    @throttle.setter
    def throttle(self, value):
        """Set the engine's throttle position.

        This value must be between 0.0 and 1.0."""
        if value > 1.0:
            value = 1.0
        elif value < 0.0:
            value = 0.0

        for i in range(self.fdmexec.GetPropulsion().GetNumEngines()):
            self.fdmexec.GetFCS().SetThrottleCmd(i, value)

class Engine(Component):
    """The Engine class contains data about the state of the aircraft's engine."""
    def __init__(self):
        Component.__init__(self)

        self.thrust = 0.0
        self.throttle = 0.0

    def update_from_fdmexec(self, fdmexec):
        engine = fdmexec.GetPropulsion().GetEngine(0)

        self.thrust = convert_libra_to_newtons(engine.GetThruster().GetThrust())

        self.throttle = fdmexec.GetFCS().GetThrottleCmd(0)

class Aircraft(object):
    """The Aircraft class is a wrapper around jsbsim that contains data about
    the aircraft state."""
    __metaclass__ = ABCMeta

    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

        self._fdmexec_state_listeners = []

        self.gps = GPS()
        self.accelerometer = Accelerometer()
        self.gyroscope = Gyroscope()
        self.thermometer = Thermometer()
        self.pressure_sensor = PressureSensor()
        self.pitot_tube = PitotTube()
        self.inertial_navigation_system = InertialNavigationSystem()
        self.engine = Engine()
        self.controls = Controls(fdmexec)

    def _update_components(self):
        fdmexec = self.fdmexec

        self.gps.update_from_fdmexec(fdmexec)
        self.accelerometer.update_from_fdmexec(fdmexec)
        self.gyroscope.update_from_fdmexec(fdmexec)
        self.thermometer.update_from_fdmexec(fdmexec)
        self.pressure_sensor.update_from_fdmexec(fdmexec)
        self.pitot_tube.update_from_fdmexec(fdmexec)
        self.inertial_navigation_system.update_from_fdmexec(fdmexec)
        self.engine.update_from_fdmexec(fdmexec)

    def set_initial_conditions(self, latitude, longitude, altitude, airspeed, heading):
        ic = self.fdmexec.GetIC()

        #ic.SetVtrueKtsIC(airspeed)
        ic.SetVcalibratedKtsIC(airspeed)
        ic.SetLatitudeDegIC(latitude)
        ic.SetLongitudeDegIC(longitude)
        ic.SetAltitudeASLFtIC(altitude)
        ic.SetPsiDegIC(heading)

        logging.debug("Initial conditions: latitude=%f, longitude=%f, altitude=%f, airspeed=%f, heading=%f",
                      latitude,
                      longitude,
                      altitude,
                      airspeed,
                      heading)

    def run(self):
        fdmexec = self.fdmexec

        fdmexec.ProcessMessage()
        fdmexec.CheckIncrementalHold()

        run_result = fdmexec.Run()

        if run_result:
            self._update_components()
        else:
            logging.error("Failed to update the fdm model")

        return run_result

    def reset(self):
        ic_result = self.fdmexec.RunIC()
        
        if not ic_result:
            logging.error("Failed to run initial condition")
            return False

        running = True
        while running and self.fdmexec.GetSimTime() < self.fdmexec.GetDeltaT() * 10:
            self.fdmexec.ProcessMessage()
            self.fdmexec.CheckIncrementalHold()

            running = self.fdmexec.Run()

        if not running:
            logging.error("Failed to execute initial run")
            return False

        engine_start = self.start_engines()

        if not engine_start:
            logging.error("Failed to start the engines")
            return False

        trim_result = self.trim()

        if not trim_result:
            logging.error("Failed to trim the aircraft")
            return False

        self._update_components()

        return True

    @abstractmethod
    def start_engines(self):
        pass

    @abstractmethod
    def trim(self):
        pass

class C172P(Aircraft):
    def __init__(self, fdmexec):
        Aircraft.__init__(self, fdmexec)

    def start_engines(self):
        engine = self.fdmexec.GetPropulsion().GetEngine(0)
        engine.SetRunning(True)

        self.fdmexec.SetPropertyValue("fcs/throttle-cmd-norm", 0.5)
        self.fdmexec.SetPropertyValue("fcs/mixture-cmd-norm", 1.0)
        self.fdmexec.SetPropertyValue("propulsion/magneto_cmd", 3.0)
        self.fdmexec.SetPropertyValue("propulsion/starter_cmd", 1.0)

        start_time = self.fdmexec.GetSimTime()
        engine_start_delay = 5.0

        running = True
        while running and self.fdmexec.GetSimTime() < start_time + engine_start_delay:
            running = self.run()

        if self.engine.thrust > 0.0:
            return running
        else:
            #return False
            return True

    def trim(self):
        self.fdmexec.DoSimplexTrim(tFull)

        return True

class Boing737(Aircraft):
    def __init__(self, fdmexec):
        Aircraft.__init__(self, fdmexec)

    def start_engines(self):
        num_engines = self.fdmexec.GetPropulsion().GetNumEngines()
        for i in range(num_engines):
            engine = self.fdmexec.GetPropulsion().GetEngine(i)
            engine.SetRunning(True)

    def trim(self):
        trimmer = FGTrim(self.fdmexec, tFull)
        trim_result = trimmer.DoTrim()

        if not trim_result:
            logging.error("Failed to trim the aircraft")

        trimmer.Report()

        return trim_result
