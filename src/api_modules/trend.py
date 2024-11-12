from flask import request, jsonify, make_response
from flask_restful import Resource
from ormWP import Woreda, Trend
from datetime import datetime

class GetTrend(Resource):
    def get(self):
        """
        Get biomass trend for a specific woreda.
        ---
        description: Fetches the biomass trend data for a specific Woreda. This endpoint needs one parameter, woreda that is ext_id of the woreda to be queried (this ext_id can be obtained from the endpoint /woreda); The API will respond with the list of the woredas covering the biomass area of interest.
        tags:
          - Biomass
        parameters:
          - in: query
            name: extId
            type: string
            required: true
            description: External Id to identify Woreda to be queried, for example ET050788
        responses:
          200:
            description: Biomass trend data
            schema:
              id: Trend
              properties:
                date:
                  type: date
                  description: Date for the trend
                mean:
                  type: float
                  description: Mean value for the trend
                
          404:
            description: Woreda not found
          422:
            description: Validation error
        """

        # Helper function for error responses
        def error_response(message, status):
            return make_response(jsonify({"error": message}), status)

        # Get extId from query parameters
        extId = request.args.get("extId")

        # Validate input
        if not extId:
            return error_response("extId is required.", 422)

        try:
            # Query woreda
            woreda = Woreda.objects(ext_id=extId).first()
            if not woreda:
                return error_response("Woreda not found.", 404)

            # Query trend data
            trend_data = (
                Trend.objects(woreda=woreda.id, date__gt=datetime(2021, 12, 19))
                .order_by("date")
                .only("date", "mean")
            )

            # If no trend data, return an empty list with a 200 status code
            if not trend_data:
                return make_response(jsonify([]), 200)

            # Prepare trend JSON response
            json_data = [{"date": str(x.date), "mean": x.mean} for x in trend_data]

            # Return the trend data
            return make_response(jsonify(json_data), 200)

        except Exception as e:
            # Handle unexpected server errors
            return error_response(f"An error occurred: {str(e)}", 500)
