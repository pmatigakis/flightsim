import logging
import os

from PyJSBSim import FGFDMExec

from huginn.aircraft import C172P, Boing737

#interface settings
SIMULATOR_CONTROL_PORT = 10500
WEB_SERVER_PORT = 8090
SENSORS_PORT = 10300
CONTROLS_PORT = 10301
FDM_CLIENT_ADDRESS = "127.0.0.1"
FDM_CLIENT_PORT = 10302
FDM_CLIENT_DT = 0.016 
TELEMETRY_PORT = 10400
TELEMETRY_DT = 0.1

#simulation settings
DT = 1.0/160.0

#initial condition
INITIAL_LATITUDE = 37.926488
INITIAL_LONGITUDE = 23.931830
INITIAL_HEADING = 45.0 #degrees
