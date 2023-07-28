from flask import Flask, jsonify
from flask_restful import Resource
from ormWP import Watershed
import json

class Watersheds(Resource):

    def __init__(self):
        super().__init__()

    def get(self,adm3=None):
        """
        Get all watershed  from database 
        ---
        description: Query the information of the watersheds. This endpoint needs one parameter, **adm3** that is id of the administrative levels 3 (kebele) to be queried (this id can be obtained from the endpoint `/adm3`); The API will respond with the list of the watersheds from that specific kebele.
        parameters:
          - in: path
            name: adm3
            type: string
            required: true
        responses:    
          200:
            description: Watersheds
            schema:
              id: watershed
              properties:
                id:
                  type: string
                  description: Id watershed
                name:
                  type: string
                  description: watershed 3 name
                adm3:
                  type: string
                  description: Id Administrative level 3
        """
        q_set = None
        if adm3 is None:
            q_set = Watershed.objects()
        else:
            print(adm3)
            q_set = Watershed.objects(adm3 = adm3)
        json_data = [{"id":str(x.id),"area":x.area,"adm3":str(x.adm3.id)} for x in q_set]
        return json_data