import os
from flask_restful import Resource
from flask import Flask, jsonify, request
from ormWP import Waterpoint, Monitored
from enum import Enum

class AdvisoryEnum_EN(Enum):
    Good = 'Good advisory, new advisories soon'
    Dry = 'Near dry advisory, new advisories soon'
    Watch = 'Watch advisory, new advisories soon' 
    Alert = 'Alert advisory, new advisories soon'
    Seasonal_dry = 'Seasonal dry advisory, new advisories soon'     
    Near_dry = 'Near dry advisory, new advisories soon'

class AdvisoryEnum_AM(Enum):
    Good = 'Good advisory, amharic'
    Dry = 'Near dry advisory, amharic'
    Watch = 'Watch advisory, amharic' 
    Alert = 'Alert advisory, amharic'
    Seasonal_dry = 'Seasonal dry advisory, amharic'     
    Near_dry = 'Near dry advisory, amharic'

class AdvisoryEnum_Oromo(Enum):
    Good = 'Good advisory, oromo'
    Dry = 'Near dry advisory, oromo'
    Watch = 'Watch advisory, oromo' 
    Alert = 'Alert advisory, oromo'
    Seasonal_dry = 'Seasonal dry advisory, oromo'     
    Near_dry = 'Near dry advisory, oromo'

class Advisory(Resource):

    def __init__(self):
        super().__init__()

    def post(self):
        """
        Get advisory.
        ---
        description: Query the information of waterpoints that match the specified advisory. This endpoint needs three parameters, **wp_status**, **waterpoints**, and **language**. The API will respond with the list of waterpoints that match the specified advisory in the specified language, the waterpoints Id can be obtained in `/waterpoint` endpoint and the wp_status only can be good,alert,watch,near_dry,seasonal_dry, and the language only can be `or`(oromo),`en`(english) and `am`(ahmaric).
        tags:
          - Advisory
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                waterpoints:
                  type: array
                  items:
                    type: string
                    properties:
                  description: "List of the waterpoints and the status"
                wp_status:
                  type: array
                  items:
                    type: string
                    properties:
                  description: "List of the waterpoints and the status"
                language:
                  type: string
                  description: "Language for the advisory text"
                  example: "en"  # Example for English, you can add more languages and handle them accordingly
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

        wp_status = data.get('wp_status')
        language = data.get('language')  # Read the language parameter
        
        if language == 'en':
            advisory_text = AdvisoryEnum_EN
        elif language == 'or':
            advisory_text = AdvisoryEnum_Oromo
        elif language == 'am':
            advisory_text = AdvisoryEnum_AM
        else:
            return {"error": f"Language '{language}' not supported"}, 400
        
        if wp_status:
            wp_status = [wp_statu.capitalize() for wp_statu in wp_status]

            for wp_statu in wp_status:
                if wp_statu not in [enum.name for enum in advisory_text]:
                    return {"error": f"Invalid advisory: {wp_statu}"}, 400
        else:
            return {"error": "No wp_status provided"}, 400

        json_data = []
        waterpoints = data.get('waterpoints')
        for waterpoint in waterpoints:
            wp=Waterpoint.objects(id=str(waterpoint)).first()
            monitored = Monitored.objects(waterpoint=wp.id).order_by('-date').limit(1).first()
            climatology=wp.climatology
            date=monitored.date
            day=date.day
            latest_monitored_depth=monitored.values[3]['value']
            month=date.month
            climatology_values=None
            current_state=None
            for c in climatology:
               if c[0]['month'] == month and c[0]['day'] == day:
                   climatology_values=c[0]['values']
            if latest_monitored_depth == 0 and climatology_values[3]["value"] == 0:
                current_state = "Seasonal_dry"
            elif latest_monitored_depth > climatology_values[3]["value"]:
                current_state = "Good"
            elif climatology_values[3]["value"] == 0:
                current_state = "Seasonal_dry"
                
            elif (latest_monitored_depth / climatology_values[3]["value"]) > 0.5:
                current_state = "Watch"
            elif (latest_monitored_depth / climatology_values[3]["value"]) > 0.03:
                current_state = "Alert"
            else:
                current_state = "Near_dry"
                
            if current_state in wp_status:
                json_data.append({"waterpointid": waterpoint, "advisory": advisory_text[current_state].value, "type_advisory": current_state})
                
        return jsonify(json_data)
