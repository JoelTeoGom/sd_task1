import grpc
from concurrent import futures
import time
import multiprocessing

import meteoServer_pb2
import meteoServer_pb2_grpc

from load_balancer_service import load_balancer_service
from processor_service import processor_service

#clase del servicio LB que delega a la clase LB serice
class LoadBalancerServiceServicer(meteoServer_pb2_grpc.LoadBalancerServiceServicer):
    def SendMeteoData(self,RawMeteoData, context):
        load_balancer_service.send_meteo_data(RawMeteoData)
        response = meteoServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()        
        return response

    def SendPollutionData(self,RawPollutionData, context):
        load_balancer_service.send_pollution_data(RawPollutionData)
        response = meteoServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response
        
class ProcessorServiceServicer(meteoServer_pb2_grpc.ProcessServiceServicer):
    def SendMeteoData(self,RawMeteoData, context):
        processor_service.send_meteo_data(RawMeteoData)
        response = meteoServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()        
        return response

    def SendPollutionData(self,RawPollutionData, context):
        processor_service.send_pollution_data(RawPollutionData)
        response = meteoServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response  
    
#metodo para lanzar los servidores que alojaran el servicio de los processors
def iniciar_servidor(port):
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        meteoServer_pb2_grpc.add_ProcessServiceServicer_to_server(ProcessorServiceServicer(), server)
        print(f'Starting server. Listening on port {port}.')
        server.add_insecure_port(f'[::]:{port}')
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)

def main():
    #=====================================================================================================
    #Servidor que contendra el loadBalancer
    #=====================================================================================================
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    meteoServer_pb2_grpc.add_LoadBalancerServiceServicer_to_server(LoadBalancerServiceServicer(), server)
    # listen on port 50051
    print('Starting server. Listening on port 50051.')
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    #=====================================================================================================

    #lanzamos los servidores que contendran los servicios de los processors
    #hay que encapsularlos en procesos porque sino solo se ejecutara el primero, se quedara en un bucle infinito
    #asi se ejecutan concurrentemente
    processes = []
    portlist = [50052, 50053, 50054]
    for port in portlist:
        p = multiprocessing.Process(target=iniciar_servidor, args=(port,))
        p.start()
        processes.append(p)


    # since server.start() will not block,
    # a sleep-loop is added to keep alive
    try:
        while True:
            server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        
        
if __name__ == "__main__":
    main()