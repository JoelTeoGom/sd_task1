import grpc
import meteoServer_pb2
import meteoServer_pb2_grpc
from meteo_utils import MeteoDataDetector
import time
import multiprocessing
from google.protobuf.timestamp_pb2 import Timestamp

# 5 de cada sensor 
N_SENS = 2

def meteo_function(sensor):
    detector = MeteoDataDetector()
    while True:
        timestamp = Timestamp()
        timestamp.seconds = int(time.time())
        meteo_data = detector.analyze_air()
        temperature = meteo_data.get('temperature')
        humidity = meteo_data.get('humidity')
        RawMeteoData = meteoServer_pb2.RawMeteoData(id=sensor,temperature=temperature,humidity=humidity, timestamp= timestamp)
        stub.SendMeteoData(RawMeteoData)
        time.sleep(2)

def pollution_function(sensor):
    detector = MeteoDataDetector()
    while True:
        timestamp = Timestamp()
        timestamp.seconds = int(time.time())
        pollution_data = detector.analyze_pollution()
        co2 = pollution_data.get('co2')
        RawPollutionData = meteoServer_pb2.RawPollutionData(id=sensor, co2=co2, timestamp= timestamp)
        stub.SendPollutionData(RawPollutionData)
        time.sleep(2)
    
# open a gRPC channel
with grpc.insecure_channel('localhost:50051') as channel:
    
    # create a stub (client)
    stub = meteoServer_pb2_grpc.MeteoServiceStub(channel)
       
    for i in range(N_SENS):
        process_name = f"SensorAir{i}"
        process = multiprocessing.Process(target=meteo_function, args=(process_name,))
        process.start()
    
    for i in range(N_SENS):
        process_name = f"SensorPol{i}"
        process = multiprocessing.Process(target=pollution_function, args=(process_name,))
        process.start()
