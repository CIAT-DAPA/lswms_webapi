from flask import request, jsonify, make_response
from flask_restful import Resource
from ormWP import Woreda, Trend
from datetime import datetime

class GetMean(Resource):
    def get(self):
        """
        Get mean biomass for a specific woreda and timestamp.
        ---
        description: Fetches the mean biomass for a specific woreda and timestamp.
        tags:
          - Biomass
        parameters:
          - in: query
            name: extId
            type: string
            required: true
            description: External Id to identify Woreda to be queried, for example ET050788
          - in: query
            name: timestamp
            type: string
            required: true
            description: Date in YYYY-MM-DD format, for example 2024-10-15
        responses:
          200:
            description: Mean biomass
            schema:
              id: Mean
              properties:
                mean:
                  type: float
                  description: Mean value for the biomass             
          404:
            description: Woreda not found
          422:
            description: Validation error
        """
        # Helper function for error responses
        def error_response(message, status):
            return make_response(jsonify({"error": message}), status)

        # Get query parameters
        extId = request.args.get("extId")
        timestamp = request.args.get("timestamp")

        # Validate input
        if not extId or not timestamp:
            return error_response("extId and timestamp are required.", 422)

        try:
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d")
        except ValueError:
            return error_response("Invalid date format. Expected YYYY-MM-DD.", 422)

        try:
            # Query woreda
            woreda = Woreda.objects(ext_id=extId).first()
            if not woreda:
                return error_response("Woreda not found.", 404)

            # Query mean biomass
            mean_biomass = Trend.objects(woreda=woreda.id, date=timestamp).only("mean").first()
            if not mean_biomass:
                return make_response(jsonify({"meanBiomass": None}), 200)

            # Return mean biomass value
            return make_response(jsonify({"meanBiomass": mean_biomass.mean}), 200)

        except Exception as e:
            # Handle unexpected server errors
            return error_response(f"An error occurred: {str(e)}", 500)
