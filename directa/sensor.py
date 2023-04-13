import grpc

# import the generated classes
import meteoServer_pb2
import meteoServer_pb2_grpc
from meteo_utils import MeteoDataDetector
import time

from google.protobuf.timestamp_pb2 import Timestamp

# 5 de cada sensor 
N_SENS = 5

# open a gRPC channel
with grpc.insecure_channel('localhost:50051') as channel:
    
    # create a stub (client)
    stub = meteoServer_pb2_grpc.MeteoServiceStub(channel)
        
    # create a valid request message
    detector = MeteoDataDetector()

    # lista de sensores
    sensores = [] 
    for i in range(N_SENS):
        sensores.append(f'AirSens{i+1}')
        sensores.append(f'PolSens{i+1}')
    
    try: 
        while True:
            for sensor in sensores:
                print(sensor)
                timestamp = Timestamp()
                timestamp.seconds = int(time.time())  
                
                if 'AirSens' in sensor:
                    meteo_data = detector.analyze_air()
                    temperature = meteo_data.get('temperature')
                    humidity = meteo_data.get('humidity')
                    RawMeteoData = meteoServer_pb2.RawMeteoData(id=sensor,temperature=temperature,humidity=humidity, timestamp= timestamp)
                    stub.SendMeteoData(RawMeteoData)
                else:
                    pollution_data = detector.analyze_pollution()
                    co2 = meteo_data.get('co2')
                    RawPollutionData = meteoServer_pb2.RawPollutionData(id=sensor, co2=co2, timestamp= timestamp)
                    stub.SendPollutionData(RawPollutionData)

            time.sleep(2)
    except KeyboardInterrupt:
        channel.close()



