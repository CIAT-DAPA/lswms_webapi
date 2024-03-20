import os
from flask_restful import Resource
import requests
from flask import Flask, jsonify, request
from ormWP import Waterpoint, Monitored
import json
import ast
from enum import Enum
class AdvisoryEnum(Enum):
    """"
    Represents the status of the waterpoint
    """
    Good= 'Good advisory, new advisorys soon'
    Dry= 'Near dry advisory, new advisorys soon'
    Watch= 'Watch advisory, new advisorys soon' 
    Alert= 'Alert advisory, new advisorys soon'
    Seasonal_dry= 'Seasonal dry advisory, new advisorys soon'     
    Near_dry= 'Near dry advisory, new advisorys soon'

class Advisory(Resource):

    def __init__(self):
        super().__init__()

    def post(self):
        """
        Get advisory.
        ---
        description: Query the information of waterpoints that match the specified advisory. This endpoint needs two parameters, **advisory** and **waterpoints**. The API will respond with the list of waterpoints that match the specified advisory, the waterpoints Id can be obtained in `/waterpoint` endpoint and the status only can be good,alert,watch,near_dry,seasonal_dry.
        tags:
          - Advisory
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                advisory:
                  type: string
                  example: "good"
                  description: "status of the waterpoint exaample, good watch, near dry, seasonal dry"
                waterpoints:
                  type: array
                  items:
                    type: string
                    properties:
                  description: "List of the waterpoints and the status" 
        responses:
          200:
            description: waterpoint_id and advisory
            schema:
              id: Advisory
              properties:
                waterpoints:
                  type: string
                  format: string
                  description: waterpoint id
                  example: 5f5e3e3e4f8b9461ac6ed74cb
                advisory:
                  type: string
                  format: string 
                  description: status of the waterpoint
                  example: good	
        """
        data = request.get_json()

        advisory = data.get('advisory')
        print(AdvisoryEnum.__members__)
        if advisory:
            if advisory[0].islower():
                advisory = advisory.capitalize()
        if advisory in AdvisoryEnum.__members__:
            print(f"passss")
            pass
        else:
            return {"error": "Invalid advisory"}, 400
        json_data = []
        waterpoints = data.get('waterpoints')
        for waterpoint in waterpoints:
            wp=Waterpoint.objects(id=str(waterpoint)).first()
            monitored = Monitored.objects(waterpoint=wp.id).order_by('-date').limit(1).first()
            climatology=wp.climatology
            date=monitored.date
            day=date.day
            latest_monnitored_depth=monitored.values[3]['value']
            month=date.month
            climatology_values=None
            current_state=None
            for c in climatology:
               if c[0]['month'] == month and c[0]['day'] == day:
                   climatology_values=c[0]['values']
            if latest_monnitored_depth	 == 0 and climatology_values[3]["value"] == 0:
                current_state = "Seasonal_dry"
            elif latest_monnitored_depth > climatology_values[3]["value"]:
                current_state = "Good"
            elif climatology_values[3]["value"] == 0:
                current_state = "Seasonal_dry"
                
            elif (latest_monnitored_depth/climatology_values[3]["value"]) > 0.5:
                current_state = "Watch"
            elif (latest_monnitored_depth/climatology_values[3]["value"]) > 0.03:
                current_state = "Alert"
            else:
                current_state = "Near_dry"
            if current_state == advisory and current_state in AdvisoryEnum.__members__:
                json_data.append({"waterpoint": waterpoint, "advisory": AdvisoryEnum[advisory].value})
        return jsonify(json_data)


