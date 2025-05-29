from flask import Flask, jsonify
from flask_restful import Resource
from ormWP import Monitored, Wpcontent, Wscontent, Waterpoint, Watershed
import json
import datetime

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
        if date is None:
            return jsonify({"error": "Date parameter is required"}), 400

        try:
            date_obj = datetime.datetime.strptime(date.split("T")[0] if "T" in date else date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        json_data = []
        all_waterpoints = Waterpoint.objects()

        for wp in all_waterpoints:
            # 1. Intentar buscar Monitored para el waterpoint en la fecha original
            monitored = Monitored.objects(waterpoint=wp.id, date__startswith=date).first()
            # 2. Si no hay datos, intentar en los 3 días anteriores
            if not monitored:
                for i in range(1, 4):
                    previous_date = (date_obj - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                    monitored = Monitored.objects(waterpoint=wp.id, date__startswith=previous_date).first()
                    if monitored:
                        break  # Encontró datos para este punto

            if not monitored:
                continue  # Este waterpoint no tiene datos en la fecha original ni en los 3 días anteriores

            water = wp
            q_setWpC = Wpcontent.objects(waterpoint=wp.id)
            q_setWsC = Wscontent.objects(watershed=water.watershed.id)
            En = Am = Or = False
            for wsc in q_setWsC:
                lang = wsc.content.get('language')
                if lang == 'en': En = True
                elif lang == 'or': Or = True
                elif lang == 'am': Am = True
            for wpc in q_setWpC:
                lang = wpc.content.get('language')
                if lang == 'en': En = True
                elif lang == 'or': Or = True
                elif lang == 'am': Am = True

            climatology_data = find_date_in_climatology(water.climatology, monitored.date.isoformat())
            monitored.values.append(climatology_data)

            if climatology_data:
                previous_values = [{"type": item["type"], "value": item["value"]} for item in monitored.values if "type" in item and "value" in item]
                climatology_values = []
                for climatology_item in climatology_data:
                    for value in climatology_item.get("values", []):
                        climatology_values.append({
                            "type": "climatology_" + value["type"],
                            "value": value["value"]
                        })
                all_values = previous_values + climatology_values

                json_data.append({
                    "id": str(monitored.id),
                    "date": monitored.date.isoformat(),
                    "source_date": monitored.date.isoformat(),
                    "values": all_values,
                    "waterpointId": str(wp.id),
                    "am": Am,
                    "en": En,
                    "or": Or
                })

        return jsonify(json_data)
