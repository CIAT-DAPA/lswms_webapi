from flask import request, jsonify, make_response
from flask_restful import Resource
from ormWP import Woreda, Trend, Forecast
from datetime import datetime

class GetForecast(Resource):
    def get(self):
        """
        Get biomass forecast for a specific woreda.
        ---
        description: Fetches the biomass forecast data for a specific Woreda. This endpoint needs one parameter, woreda that is ext_id of the woreda to be queried (this ext_id can be obtained from the endpoint /woreda); The API will respond with the list of the woredas covering the biomass area of interest.
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
            description: Biomass forecast data
            schema:
              id: Forecast
              properties:
                date:
                  type: date
                  description: Date for the forecast
                mean:
                  type: float
                  description: Mean value for the forecast            
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

            # Query latest trend
            latest_trend = (
                Trend.objects(woreda=woreda.id)
                .order_by("-date")
                .only("date", "mean")
                .first()
            )

            # Query forecast data
            forecast_data = (
                Forecast.objects(woreda=woreda.id)
                .order_by("-date")
                .only("date", "mean")
                .limit(3)
            )

            # Prepare forecast JSON response
            json_forecast = [{"date": x.date.strftime("%Y-%m-%d"), "mean": x.mean} for x in forecast_data]

            if latest_trend:
                json_forecast.append(
                    {"date": latest_trend.date.strftime("%Y-%m-%d"), "mean": latest_trend.mean}
                )

            # Sort forecast data by date
            json_forecast.sort(key=lambda x: x["date"])

            # Return the forecast data
            return make_response(jsonify(json_forecast), 200)

        except Exception as e:
            # Handle unexpected errors
            return error_response(f"An error occurred: {str(e)}", 500)
