from flask_restful import Resource
from flask import Flask, jsonify, request
from ormWP import Waterpoint, Monitored
from enum import Enum
import datetime

def find_date_in_climatology(climatology, target_date):
    target_datetime = datetime.datetime.strptime(target_date, "%Y-%m-%dT%H:%M:%S")
    target_month = target_datetime.month
    target_day = target_datetime.day
    
    for daily_data in climatology:
        if daily_data[0]['month'] == target_month and daily_data[0]['day'] == target_day:
            return daily_data
    return None
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
    Good = 'Haroon  haala dansaa irra jira. Kanafuu bishaani kana seeran dhimmoota adda addaaf itti fayyadamu.'
    Watch = 'Haroon  xiqqachaa jira. Kanafuu bishaani dhimmotaa adda addaaf itti fayyadamnu hir’isuu akkasumass abbaan herregaa hordofi tasisuu qaba.'
    Alert = 'Haroon  akka maale xiqqatee jira. Kanafuu bishaan kana dhugaatii fi beellada dadhaboo qofaaf fayyadamu.'
    Seasonal_dry = 'Haroon  gogee/foqaate jira. kanafuu ummatini gara bishaan jirutii godanuu qabu.'
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
            climatology_data= find_date_in_climatology(wp.climatology, monitored.date.isoformat())
            latest_monitored_depth = monitored.values[0]['value']
            current_state = None
            if latest_monitored_depth >= 0.7:
                current_state = "Good"
            elif latest_monitored_depth ==0 and climatology_data[0]['values'][0]['value'] == 0:
                current_state = "Seasonal_dry"
            elif latest_monitored_depth >= 0 and climatology_data[0]['values'][0]['value'] < 0.2:
                current_state = "Near_dry"
            elif latest_monitored_depth >= 0.2 and climatology_data[0]['values'][0]['value'] < 0.3:
                current_state = "Alert"
            elif latest_monitored_depth >= 0.3 and climatology_data[0]['values'][0]['value'] < 0.7:
                current_state = "Watch"
            
            else:
                current_state = "Good"
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
