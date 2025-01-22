from flask import Flask, jsonify
from flask_restful import Resource
from ormWP import Monitored, Wpcontent, Wscontent, Waterpoint, Watershed
import json

import datetime
from flask import jsonify

def find_date_in_climatology(climatology, target_date):
    target_datetime = datetime.datetime.strptime(target_date.split("T")[0] if "T" in target_date else target_date, "%Y-%m-%d")
    target_month = target_datetime.month
    target_day = target_datetime.day

    for daily_data in climatology:
        if daily_data[0]['month'] == target_month and daily_data[0]['day'] == target_day:
            return daily_data
    return None

class LastMonitoredDataByDate(Resource):
    def __init__(self):
        super().__init__()

    def get(self, date=None):
        """
        Get last Monitored data by date
        ---
        description: Query the information of last monitored data based on a specific date. This endpoint needs one parameter, **date**, that is the date in format YYYY-MM-DD to be queried. The API will respond with the list of monitored values for that specific date.
        tags:
          - Monitored Data by Date
        parameters:
          - in: path
            name: date
            type: string
            required: true
            description: Date to query in format YYYY-MM-DD, for example 2024-01-29
        responses:
          200:
            description: Monitored data
            schema:
              id: Monitored
              properties:
                id:
                  type: string
                  description: Id Monitored data
                date:
                  type: string
                  description: Date of the monitored data
                values:
                  type: array
                  items: {}
                  description: List of values of the monitored data
                waterpoint:
                  type: string
                  description: Id waterpoint
        """

        if date is None:
            return jsonify({"error": "Date parameter is required"}), 400

        try:
            target_datetime = datetime.datetime.strptime(date.split("T")[0] if "T" in date else date, "%Y-%m-%d")
        except ValueError as e:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        q_set = Monitored.objects(date__startswith=date)

        json_data = []

        for x in q_set:
            waterpoint = x.waterpoint
            water = Waterpoint.objects(id=waterpoint.id).first()
            q_setWpC = Wpcontent.objects(waterpoint=waterpoint.id)
            q_setWsC = Wscontent.objects(watershed=water.watershed.id)

            En = False
            Am = False
            Or = False

            for wsc in q_setWsC:
                if wsc.content['language'] == 'en':
                    En = True
                elif wsc.content['language'] == 'or':
                    Or = True
                elif wsc.content['language'] == 'am':
                    Am = True

            for wpc in q_setWpC:
                if wpc.content['language'] == 'en':
                    En = True
                elif wpc.content['language'] == 'or':
                    Or = True
                elif wpc.content['language'] == 'am':
                    Am = True

            climatology_data = find_date_in_climatology(water.climatology, x.date.isoformat())
            x.values.append(climatology_data)

            if climatology_data:
                previous_values = [{"type": item["type"], "value": item["value"]} for item in x.values if "type" in item and "value" in item]

                climatology_values = []
                for climatology_item in climatology_data:
                    for value in climatology_item.get("values", []):
                        climatology_values.append({
                            "type": "climatology_" + value["type"],
                            "value": value["value"]
                        })

                all_values = previous_values + climatology_values

                json_data.append({
                    "id": str(x.id),
                    "date": x.date.isoformat(),
                    "values": all_values,
                    "waterpointId": str(waterpoint.id),
                    "am": Am,
                    "en": En,
                    "or": Or
                })

        return jsonify(json_data)
