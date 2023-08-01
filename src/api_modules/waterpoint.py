from flask import Flask, jsonify
from flask_restful import Resource
from ormWP import Waterpoint
import json

class Waterpoints(Resource):

    def __init__(self):
        super().__init__()

    def get(self):
        """
        Get all waterpoints  from database 
        ---
        description: Query the information of the waterpoints. This endpoint has not parameter.
        responses:    
          200:
            description: Waterpoints
            schema:
              id: Waterpoints
              properties:
                id:
                  type: string
                  description: Id Waterpoints
                name:
                  type: string
                  description: Waterpoint name
                ext_id:
                  type: string
                  description: Extern Id to identify Waterpoin
                lat:
                  type: number
                  description: latitude of the Waterpoint
                lon:
                  type: number
                  description: longityde of the Waterpoint
                area:
                  type: number
                  description: area of the Waterpoint
                watershed:
                  type: string
                  description: Id watershed
        """
        q_set = None
        q_set= Waterpoint.objects()
        json_data = [{"id":str(x.id),"name":x.name,"lat":x.lat,"lon":x.lon,"area":x.area,"ext_id":str(x.ext_id),"climatology":x.climatology,"watershed":str(x.watershed.id)} for x in q_set]
        return json_data