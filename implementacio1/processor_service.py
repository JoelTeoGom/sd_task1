import random
from queue import Queue
import multiprocessing
from meteo_utils import MeteoDataProcessor

class meteoData:
    def __init__(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity
        
class pollutionData:  
    def __init__(self, co2):
        self.co2 = co2
        
class processorService:
    def __init__(self):
        self.processor = MeteoDataProcessor()
         
    def process_meteo_data(self,RawMeteoData):
        # process_meteo_data expects RawMeteoData: an object
        # with the attributes temperature and humidity
        print(RawMeteoData)
        return 'Done'
    
    def process_pollution_data(self,RawPollutionData):
        # process_pollution_data expects RawPollutionData: an object
        # with the attribute co2
        #pollution_data = self.processor.process_pollution_data(pollution_data)
        print(RawPollutionData) 
        return 'Done'

processor_service = processorService()