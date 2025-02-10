import json
import time  # Para medir el tiempo de respuesta
from flask import Flask, jsonify, make_response
from flask_restful import Resource
from ormWP import Monitored

class MonitoredData(Resource):

    def __init__(self):
        super().__init__()

    def get(self, waterpoint=None):
        """
        Get all Monitored data
        ---
        description: Query the information of monitored data from one waterpoint. This endpoint needs one parameter, **waterpoint**, which is the id of the waterpoint to be queried (this id can be obtained from the endpoint `/waterpoint`). The API will respond with the list of monitored values from that specific waterpoint.
        tags:
          - Waterpoint Monitored data
        parameters:
          - in: path
            name: waterpoint
            type: string
            required: true
            description: Waterpoint ID to be queried, for example 64d1bf1cc703fe54e05ee7d6
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

        start_time = time.time()  

        q_set = Monitored.objects(waterpoint=waterpoint) if waterpoint else Monitored.objects(trace__enabled=True)

        response_data = [
            {"id": str(x.id), "date": x.date.isoformat(), "values": x.values, "waterpointId": waterpoint}
            for x in q_set
        ]

        end_time = time.time() 
        response_time_ms = (end_time - start_time) * 1000  

        response = make_response(jsonify(response_data), 200)
        response.headers["X-Response-Time"] = f"{response_time_ms:.2f} ms"

        return response
