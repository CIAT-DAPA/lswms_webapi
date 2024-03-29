from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd
import os
from ormWP import Waterpoint, Monitored
from conf import config


API_KEY = config['API_KEY']

class ProtectedEndpoint(Resource):
    def __init__(self):
        super().__init__()

    def post(self):
        """
        Update the database with new data.

        ---
        tags:
          - ETL
        parameters:
          - in: header
            name: Authorization
            type: string
            required: true
            description: Password in format "Bearer secret_key"
          - in: body
            name: json
            description: DataFrame in JSON
            required: true
            schema:
              type: object
              examples:
                example-1:
                  value: {"location_id": 1, "date": 1614556800000, "rain": 0.0, "evap": 0.0, "depth": 0.0, "scaled_depth": 0.0}


        responses:
          200:
            description: Data updated successfully
          401:
            description: Unauthorized - Invalid or missing password
          500:
            description: Internal server error
        """
        try:
            # Verificar la autenticación mediante la clave en el header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return {"error": "Unauthorized"}, 401

            received_api_key = auth_header.split(" ")[1]
            if received_api_key != API_KEY:
                return {"error": "Invalid API key"}, 401

            # Si la autenticación es exitosa, procesar el DataFrame
            data = request.get_json()
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'], unit='ms')
            print(df)
            def etl_monitored(df):
              count=0
              print('importing monitored waterpoint to the database')
              from datetime import datetime
              for index, row in df.iterrows():
                  #get the date value for each row
                  d=row['date']
                  #get the collection object filted with the date value
                  monitor_object=Monitored.objects(date=datetime(d.year, d.month, d.day))
                  #if the date object returns nothing, import the row
                  if len(monitor_object)==0:
                      waterpoint=Waterpoint.objects.get(ext_id=str(row['location_id']))
                      print('importing', waterpoint.name, d ,'monitored data')
                      values_list= [{'type': 'depth', 'value':row['depth']}, {'type': 'evp', 'value': row['evap']},{'type': 'rain', 'value': row['rain']},{'type': 'scaled_depth', 'value': row['scaled_depth']}
                      ]
                      monitored = Monitored(
                          date=row['date'],
                          values=values_list,
                          waterpoint=waterpoint
                      )
                      monitored.save()
                      count+=1
                  else:
                      #this list used to avoid repeated data import.
                      #it checks if the ext_id and date are already in the recored 
                      monitor_list=[i.waterpoint.ext_id for i in monitor_object]
                      #if the location id for the specifed date row['date'] is not in the the monitor_list excute the import process
                      if (str(row['location_id']) not in monitor_list):
                          waterpoint=Waterpoint.objects.get(ext_id=str(row['location_id']))
                          print('importing', waterpoint.name,'recored date ',d,' monitored data')
                          values_list= [{'type': 'depth', 'value':row['depth']}, {'type': 'evp', 'value': row['evap']},{'type': 'rain', 'value': row['rain']},{'type': 'scaled_depth', 'value': row['scaled_depth']}
                          ]
                          monitored = Monitored(
                          date=d,
                          values=values_list,
                          waterpoint=waterpoint
                          )
                          monitored.save()
                          count+=1

                      else:
                          print(f"'recored date '{d} not imported already in the database")


              return count
            etl_monitored(df)
            return {"message": "DataFrame received and processed successfully"}

        except Exception as e:
            return {"error": str(e)}, 500

