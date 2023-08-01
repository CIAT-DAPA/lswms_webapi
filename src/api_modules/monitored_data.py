from flask import Flask, jsonify
from flask_restful import Resource
from ormWP import Monitored
import json
class MonitoredData(Resource):

    def __init__(self):
        super().__init__()

    def get(self, waterpoint=None):
        """
        Get all Monitored data
        ---
        description: Query the information of monitored data from one waterpoint . This endpoint needs one parameter, **waterpoint** that is id of the waterpoint to be queried (this id can be obtained from the endpoint `/waterpoint`); The API will respond with the list of the monitored values from that specific waterpoint.
        parameters:
          - in: path
            name: waterpoint
            type: string
            required: true
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
        q_set = None
        if waterpoint is None:
            q_set = Monitored.objects()
        else:
            print(waterpoint)
            q_set = Monitored.objects(waterpoint = waterpoint)
        json_data = [{"id": str(x.id), "date": x.date.isoformat(), "values": x.values} for x in q_set]


        return json_data



