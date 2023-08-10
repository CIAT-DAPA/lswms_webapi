from flask import Flask, jsonify
from flask_restful import Resource
from ormWP import Waterpoint
import json

class SingleWaterpoints(Resource):

    def __init__(self):
        super().__init__()

    def get(self,waterpoint=None):
        """
        Get all one waterpoint from database 
        ---
        description: Query the information of the ons specific waterpoint. This endpoint needs one parameter, **waterpoint** that is id of the waterpoint to be queried (this id can be obtained from the endpoint `/waterpoints`); The API will respond with the waterpoit with the id provided.
        parameters:
          - in: path
            name: waterpoint
            type: string
            required: true
        responses:    
          200:
            description: Waterpoint
            schema:
              id: waterpoint
              properties:
                id:
                  type: string
                  description: Id waterpoint
                name:
                  type: string
                  description: waterpoint name
                lat:
                  type: float
                  description: latitute of the waterpoint
                lon:
                  type: float
                  description: longitude of the waterpoint
                area:
                  type: float
                  description: area of the waterpoint
                ext_id:
                  type: float
                  description: external id of the waterpoint
                watershed:
                  type: string
                  description: Id watershed
        """
        q_set = None
        if waterpoint is None:
            q_set = Waterpoint.objects()
        else:
            print(waterpoint)
            q_set = Waterpoint.objects(id = waterpoint)
        json_data = [{"id":str(x.id),"name":x.name,"lat":x.lat,"lon":x.lon,"area":x.area,"ext_id":str(x.ext_id),"climatology":x.climatology,"watershed":str(x.watershed.id),"aclimate_id":x.aclimate_id} for x in q_set]

        return json_data