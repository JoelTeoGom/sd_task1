import grpc
from concurrent import futures
import time

import meteoServer_pb2
import meteoServer_pb2_grpc

from meteo_service import meteo_service

   
class MeteoServiceServicer(meteoServer_pb2_grpc.MeteoServiceServicer):
    def SendMeteoData(self,RawMeteoData, context):
        meteo_service.send_meteo_data(RawMeteoData)
        response = meteoServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()        
        return response

    def SendPollutionData(self,RawPollutionData, context):
        meteo_service.send_pollution_data(RawPollutionData)
        response = meteoServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response
        
    
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

meteoServer_pb2_grpc.add_MeteoServiceServicer_to_server(MeteoServiceServicer(), server)


# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('0.0.0.0:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        server.wait_for_termination()
except KeyboardInterrupt:
    server.stop(0)