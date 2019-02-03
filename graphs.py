import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np
import math

from datetime import datetime, timedelta
from db_connect import db_connect


class SensorGrapher():
    def __init__(self):
        self.cur = db_connect()
        self.query = """
        SELECT time_stamp
            , values_json -> 'temperature_F' as temp
            , values_json -> 'humidity' as humid
            , values_json -> 'sunlight' as light 
            , values_json -> 'top_soil' as top_soil
            , values_json -> 'mid_soil' as mid_soil
            , values_json -> 'tray' as tray
        FROM sensor_json"""
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def fetch_df(self):
        cur.execute(sensor_query)
        data = cur.fetchall()
        df = pd.DataFrame(np.array(data))
        df.columns = ['time_stamp', 'temp', 'humid', 'light', 'top_soil', 'mid_soil', 'tray']
        df['time_stamp'] = pd.to_datetime(df.time_stamp)
        df = df.set_index('time_stamp')
        self.df = df[df.time_stamp >= (datetime.now()-timedelta(days=14))]

    def plot_moisture_data(self):
        moist_df = self.df[['tray','top_soil', 'mid_soil']]
        moist_df = moist_df[['top_soil', 'mid_soil', 'tray']].mask(df < 350)
        fig, axs = plt.subplots(1, 1, figsize=(15,5))
        axs.plot(moist_df.index, ((moist_df[['top_soil', 'mid_soil', 'tray']]/(-1024))+1))
        axs.set_title('Moisture Sensors\n timestamp: '+timestamp)
        axs.set_ylabel('Soil Moisture Readings \n 1 is completely soaked')
        axs.legend(moist_df.columns)
        axs.grid(True)
        plt.savefig('static/moisture.png')

    def plot_temp_data(self):
        pdf = self.df[['temp']]
        fig, axs = plt.subplots(1, 1, figsize=(15,5))
        axs.plot(pdf, color='red')
        axs.set_title('Temperature (F)\n UTC timestamp: '+timestamp)
        axs.set_ylabel('Temp in Degrees F')
        axs.legend(pdf.columns)
        axs.grid(True)
        plt.savefig('static/temp.png')

    def plot_humid_data(self):
        pdf = self.df[['humid']]
        fig, axs = plt.subplots(1, 1, figsize=(15,5))
        axs.plot(pdf, color='lightblue')
        axs.set_title('Humidity\n UTC timestamp: '+timestamp)
        axs.set_ylabel('Rel. Humidity (%)')
        axs.legend(pdf.columns)
        axs.grid(True)
        plt.savefig('static/humid.png')

    def plot_light_data(self):
        pdf = self.df[['light']]
        fig, axs = plt.subplots(1, 1, figsize=(15,5))
        axs.plot(pdf, color='orange')
        axs.set_title('Sunlight\n UTC timestamp: '+timestamp)
        axs.set_ylabel('Reading from LDR, unsure of unit')
        axs.legend(pdf.columns)
        axs.grid(True)
        plt.savefig('static/light.png')

if __name__ == "__main__":
    grapher = SensorGrapher()
    grapher.fetch_df()
    grapher.plot_moisture_data()    
    grapher.plot_temp_data()
    grapher.plot_light_data()
    grapher.plot_humid_data()    
    
