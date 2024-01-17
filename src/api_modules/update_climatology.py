from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd
import os
from ormWP import Waterpoint, Monitored


API_KEY = "prueba"

class ProtectedEndpointClimatology(Resource):
    def __init__(self):
        super().__init__()

    def post(self):
        """
        Update daily climatology.

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
            description: DataFrame in JSON format
            required: true
            schema:
              type: object
              example: {"col1": [1, 2, 3], "col2": ["A", "B", "C"]}

        responses:
          200:
            description: Climatology updated successfully
          401:
            description: Unauthorized - Password invalid or missing
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
            df=df.assign(month=df.date.dt.month,day=df.date.dt.day)
            df_filterd=df[['location_id','month_day','month','day','rain', 'evap','depth', 'scaled_depth']]
            df_grouped=df_filterd.groupby(['location_id','month_day']).median().reset_index()
            df_grouped=df_grouped.drop(columns=['month_day'])
            def etl_monitored(df_grouped):
                count = 0
                print('Running the update function')
                from datetime import datetime
                for i in df_grouped.location_id.unique():
                    climate = []
                    for index, row in df_grouped[df_grouped['location_id'] == i].iterrows():
                        trace = {"created": datetime.now(), "updated": datetime.now(), "enabled": True}
                        values_list = [{'type': 'depth', 'value': row['depth']}, {'type': 'evp', 'value': row['evap']},
                                        {'type': 'rain', 'value': row['rain']},{'type': 'scaled_depth', 'value': row['scaled_depth']}]
                        climate_list = [{"month": row['month'], "day": row['day'], "values": values_list}]
                        climate.append(climate_list)
                    try:
                        wp = Waterpoint.objects.get(ext_id=str(int(row['location_id'])))
                        print('Updating climatology subset', wp.name)
                        wp.update(climatology=climate, trace=trace)
                        count += 1
                    except Exception as e:
                        print(f'Error while updating climatology for waterpoint {row["location_id"]}: {str(e)}')

                print(f'Updated {count} waterpoints with climatology data in the database')
                            
            etl_monitored(df_grouped)
            
            return {"message": "DataFrame received and processed successfully"}

        except Exception as e:
            return {"error": str(e)}, 500

