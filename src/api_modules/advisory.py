from flask_restful import Resource
from flask import jsonify, request
from ormWP import Waterpoint, Monitored
from ormWP import Advisory  # tu modelo AdvisoryText
import datetime

def find_date_in_climatology(climatology, target_date):
    target_datetime = datetime.datetime.strptime(target_date, "%Y-%m-%dT%H:%M:%S")
    target_month = target_datetime.month
    target_day = target_datetime.day
    
    for daily_data in climatology:
        if daily_data[0]['month'] == target_month and daily_data[0]['day'] == target_day:
            return daily_data
    return None


class AdvisoryEndpoint(Resource):

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
                  description: "List of the waterpoints"
                advisories:
                  type: array
                  items:
                    type: string
                  description: "List of the advisories"
                language:
                  type: array
                  items:
                    type: string
                  description: "List of languages for the advisory text"
                  example: ["en", "or", "am"]  # Example for English, Oromo, and Amharic
        responses:
          200:
            description: waterpoint_id, advisory, and language
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
                language:
                  type: string
                  description: Language of the advisory text
                  example: en
        """
        data = request.get_json()
        advisories = data.get('advisories')
        languages = data.get('language')
        waterpoints = data.get('waterpoints')

        advisories_allowed = ["wp_status"]

        if not languages:
            return {"error": "No languages provided"}, 400
        if not advisories:
            return {"error": "No advisories provided"}, 400
        for advisory in advisories:
            if advisory not in advisories_allowed:
                return {"error": f"Advisory '{advisory}' not supported"}, 400

        json_data = []

        for waterpoint in waterpoints:
            wp = Waterpoint.objects(id=str(waterpoint)).first()
            if not wp:
                continue

            wp_name = wp.name
            monitored = Monitored.objects(waterpoint=wp.id).order_by('-date').limit(1).first()
            climatology_data = find_date_in_climatology(wp.climatology, monitored.date.isoformat())
            latest_monitored_depth = monitored.values[0]['value']

            # --- determinar estado actual ---
            if latest_monitored_depth >= 0.7:
                current_state = "GOOD"
            elif latest_monitored_depth == 0 and climatology_data[0]['values'][0]['value'] == 0:
                current_state = "SEASONAL_DRY"
            elif latest_monitored_depth >= 0 and climatology_data[0]['values'][0]['value'] < 0.2:
                current_state = "NEAR_DRY"
            elif latest_monitored_depth >= 0.2 and climatology_data[0]['values'][0]['value'] < 0.3:
                current_state = "ALERT"
            elif latest_monitored_depth >= 0.3 and climatology_data[0]['values'][0]['value'] < 0.7:
                current_state = "WATCH"
            else:
                current_state = "GOOD"

            # --- buscar textos en BD ---
            advisory_doc = Advisory.objects(state=current_state).first()
            if not advisory_doc:
                continue

            for lang in languages:
                if lang not in advisory_doc.languages:
                    return {"error": f"Language '{lang}' not supported"}, 400

                text = wp_name + " " + advisory_doc.languages[lang]
                json_data.append({
                    "waterpointid": waterpoint,
                    "advisory": text,
                    "wp_status": current_state,
                    "language": lang,
                    "type_advisory": ', '.join(advisory for advisory in advisories if advisory in advisories_allowed)
                })

        return jsonify(json_data)
