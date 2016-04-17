from unittest import TestCase

from huginn import configuration
from huginn.unit_conversions import convert_feet_to_meters 
from huginn.fdm import FDMBuilder
from huginn.sensors import Sensors, Accelerometer

class AccelerometerTests(TestCase):
    def test_accelerometer(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        accelerometer = Accelerometer(fdmexec)

        self.assertAlmostEqual(accelerometer.x, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(1)))
        self.assertAlmostEqual(accelerometer.y, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(2)))
        self.assertAlmostEqual(accelerometer.z, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(3)))

class SensorTests(TestCase):
    def test_accelerometer(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        sensors = Sensors(fdmexec)

        self.assertAlmostEqual(sensors.accelerometer.x, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(1)))
        self.assertAlmostEqual(sensors.accelerometer.y, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(2)))
        self.assertAlmostEqual(sensors.accelerometer.z, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(3)))
