from flask_restful import Resource
from flask import jsonify
from ormWP import Waterpoint, SeasonalForecast, SubseasonalForecast
from mongoengine import DoesNotExist


class WaterpointForecast(Resource):

    def __init__(self):
        super().__init__()

    def get(self, waterpoint_id):
        """
        Get latest seasonal and subseasonal forecasts for a waterpoint.
        ---
        description: >
          Get the most recent seasonal and subseasonal forecast for a specific waterpoint,
          based on the latest year and month available.
        tags:
          - Forecasts
        parameters:
          - in: path
            name: waterpoint_id
            required: true
            type: string
            description: Waterpoint id.
        responses:
          200:
            description: Latest seasonal and subseasonal forecasts for the waterpoint.
            schema:
              id: WaterpointForecast
              properties:
                waterpoint_id:
                  type: string
                waterpoint_name:
                  type: string
                seasonal:
                  type: object
                  properties:
                    year:
                      type: integer
                    month:
                      type: integer
                    measure:
                      type: string
                    lower:
                      type: number
                    normal:
                      type: number
                    upper:
                      type: number
                subseasonal:
                  type: object
                  properties:
                    year:
                      type: integer
                    month:
                      type: integer
                    weeks:
                      type: array
                      items:
                        type: object
                        properties:
                          week:
                            type: integer
                          measure:
                            type: string
                          lower:
                            type: number
                          normal:
                            type: number
                          upper:
                            type: number
          404:
            description: Waterpoint not found
        """

        # 1. Buscar el waterpoint (solo habilitados si usas trace.enabled)
        wp = Waterpoint.objects(id=waterpoint_id, trace__enabled=True).first()
        if not wp:
            return {"message": "Waterpoint not found"}, 404

        # 2. Seasonal más reciente (por año y mes)
        latest_seasonal = (
            SeasonalForecast.objects(waterpoint=wp)
            .order_by("-year", "-month")  # más nuevo primero
            .first()
        )

        seasonal_data = None
        if latest_seasonal and latest_seasonal.probabilities:
            p = latest_seasonal.probabilities
            seasonal_data = {
                "year": latest_seasonal.year,
                "month": latest_seasonal.month,
                "measure": p.measure,
                "lower": p.below,
                "normal": p.normal,
                "upper": p.above,
            }

        # 3. Subseasonal más reciente: buscar último año/mes y luego sus 4 semanas
        latest_sub = (
            SubseasonalForecast.objects(waterpoint=wp)
            .order_by("-year", "-month")  # más nuevo primero
            .first()
        )

        subseasonal_data = None
        if latest_sub:
            year = latest_sub.year
            month = latest_sub.month

            # todas las semanas para ese año/mes
            weeks_qs = (
                SubseasonalForecast.objects(waterpoint=wp, year=year, month=month)
                .order_by("week")
            )

            weeks_list = []
            for ss in weeks_qs:
                if ss.probabilities:
                    p = ss.probabilities
                    weeks_list.append({
                        "week": ss.week,
                        "measure": p.measure,
                        "lower": p.below,
                        "normal": p.normal,
                        "upper": p.above,
                    })

            subseasonal_data = {
                "year": year,
                "month": month,
                "weeks": weeks_list,
            }

        # 4. Armar respuesta final
        response = {
            "waterpoint_id": str(wp.id),
            "waterpoint_name": wp.name,
            "seasonal": seasonal_data,
            "subseasonal": subseasonal_data,
        }

        return response, 200