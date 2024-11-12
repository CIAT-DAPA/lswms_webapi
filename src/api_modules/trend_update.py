from flask import request, jsonify, make_response
from flask_restful import Resource
from ormWP import Woreda, Trend
from datetime import datetime
from conf import config

API_KEY = config['API_KEY']

class TrendUpdate(Resource):
    def post(self):
        """
        Save or update multiple biomass trend records to the database.
        ---
        description: Receives an array of biomass trend data and saves them to the trends collection. If a trend record with the same woreda and date exists, it updates the mean; otherwise, it creates a new record.
        tags:
          - Biomass
        parameters:
          - in: header
            name: Authorization
            type: string
            required: true
            description: Password in format "Bearer secret_key"
          - in: body
            name: body
            required: true
            schema:
              type: array
              items:
                type: object
                properties:
                  extId:
                    type: string
                    description: Woreda external ID
                  mean:
                    type: number
                    description: Biomass mean
                  date:
                    type: string
                    description: Date in YYYY-MM-DD format
        responses:
          201:
            description: Trends saved or updated successfully.
          400:
            description: Validation error.
          401:
            description: Unauthorized - Invalid or missing API key.
        """
        try:
            # Authentication verification
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return make_response(jsonify({"error": "Unauthorized"}), 401)

            received_api_key = auth_header.split(" ")[1]
            if received_api_key != API_KEY:
                return make_response(jsonify({"error": "Invalid API key"}), 401)

            # Parse JSON body
            data = request.get_json()

            if not isinstance(data, list):
                return make_response(jsonify({"error": "Expected an array of records"}), 400)

            for record in data:
                extId = record.get("extId")
                mean = record.get("mean")
                date = record.get("date")

                # Validate input
                if not extId or mean is None or not date:
                    return make_response(jsonify({"error": f"Invalid data: {record}"}), 400)

                woreda = Woreda.objects(ext_id=extId).first()
                if not woreda:
                    return make_response(jsonify({"error": f"Woreda not found for extId {extId}"}), 404)

                # Check if the trend exists
                trend_date = datetime.strptime(date, "%Y-%m-%d")
                trend = Trend.objects(woreda=woreda.id, date=trend_date).first()

                if trend:
                    # Update the existing trend
                    trend.mean = round(mean, 4)  
                    trend.save()
                else:
                    # Create a new trend record
                    trend = Trend(
                        woreda=woreda.id,
                        mean=round(mean, 4),
                        date=trend_date
                    )
                    trend.save()

            return make_response(jsonify({"message": "All trends saved or updated successfully"}), 201)

        except Exception as e:
            return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), 500)
