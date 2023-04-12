import random
from queue import Queue

class meteoService:

    def __init__(self):
        self.lb_queue = Queue()

    def send_meteo_data(self,RawMeteoData):
        print (RawMeteoData)
        self.lb_queue.put(RawMeteoData.id)
        return 'Done'
    
    def send_pollution_data(self,RawPollutionData):
        self.lb_queue.put(RawPollutionData)
        return 'Done'


meteo_service = meteoService()