from flask_restful import Resource
from flask import Flask, jsonify, request
from ormWP import Waterpoint, Monitored
from enum import Enum

class AdvisoryEnum_EN(Enum):
    Good = 'pond is in Good condition. Manage the water consumption for other purposes'
    Watch = 'pond is in Watch condition. Reduce pond water consumption for other purposes and follow pond manager instructions' 
    Alert = 'pond is in Alert condition and advised to use the pond water for drinking and weak animals only'
    Seasonal_dry = 'pond is in Dry condition. please text “ponds” to get nearby available ponds'     
    Near_dry = 'pond is in Near-Dry condition and advised to use the pond water for drinking'

class AdvisoryEnum_AM(Enum):
    Good = 'መልካም ምድብ በጣም እንቅስቃሴ ያለበት። ሌላ በምንደርሰው ደህንነት ተጠቃሚዎች የሚያስተምሩ።'
    Watch = 'ምድብ አለመታየት ነው። እናተግባረሽ ደህንነት እና ምድብ ማንኛውም ተጠቃሚ ቅጥርን ተጠቅመን ይስጡ።'
    Alert = 'መልኩ ምድብ አለመታየት ነው እና ሥሩን በምንደርሰው ደህንነት ይዞ የመጠጥ እና የቆመውን አንቀላፍ ይናገራል።'
    Seasonal_dry = 'ምድብ አለመታየት ነው። እባክዎ ከታች አቅርቦ እንደሚያደርግ “ponds” ተጠቅመው ይላኩ።'
    Near_dry = 'ምድብ ከተባለ ሁኔታ ነው እና በመጠበቅ የሚጠጡትን ምድብ ይዞ እንደሚያቆመው ያስችላል።'


class AdvisoryEnum_Oromo(Enum):
    Good = 'Hagayaan hunda qabduun sii dhiyaatee. Miidiyaan namoota akkaataa barbaadan hirmaannee jira.'
    Watch = 'Hagayaa hunda qabduun sii dhiyaate. Miidiyaan namoota akkaataa barbaachisuun barbaaddeebi’uu hunda keessatti akka dandeettii hirmaannee jira.'
    Alert = 'Hagayaan hunda qabduun sii dhiyaate. Hunda keenyaan namoota akkaataa barbaaddeebi’uu dandeettii jiran keessaa bara ministeeraa hundaa dandeessan.'
    Seasonal_dry = 'Hagayaan hunda qabduun sii dhiyaatee. Daandiiwwaan isaa ‘ponds’ akkaanuma barbaachisaa barbaadan dabalatee jira.'
    Near_dry = 'Hagayaan hunda qabduun sii dhiyaatee. Miidiyaan namoota akkaataa barbaadan hirmaannee jira.'


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
        advisories_allowed = ["wp_status"]
        if not languages:
            return {"error": "No languages provided"}, 400
        if advisories:
            for advisory in advisories:
                if advisory not in advisories_allowed:
                    return {"error": f"Advisory '{advisory}' not supported"}, 400
        else:
            return {"error": "No advisories provided"}, 400
            

        json_data = []
        waterpoints = data.get('waterpoints')
        for waterpoint in waterpoints:
            wp = Waterpoint.objects(id=str(waterpoint)).first()
            wp_name = wp.name
            monitored = Monitored.objects(waterpoint=wp.id).order_by('-date').limit(1).first()
            climatology = wp.climatology
            date = monitored.date
            day = date.day
            latest_monitored_depth = monitored.values[3]['value']
            month = date.month
            climatology_values = None
            current_state = None
            for c in climatology:
                if c[0]['month'] == month and c[0]['day'] == day:
                    climatology_values = c[0]['values']
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
              
            for lang in languages:
                if lang == 'en':
                    advisory_text = AdvisoryEnum_EN
                elif lang == 'or':
                    advisory_text = AdvisoryEnum_Oromo
                elif lang == 'am':
                    advisory_text = AdvisoryEnum_AM
                else:
                    return {"error": f"Language '{lang}' not supported"}, 400

                text = wp_name + " " + advisory_text[current_state].value
                json_data.append({"waterpointid": waterpoint, "advisory": text, "wp_status": current_state.upper(), "language": lang, "type_advisory": ', '.join(advisory for advisory in advisories if advisory in advisories_allowed)})

                
        return jsonify(json_data)
