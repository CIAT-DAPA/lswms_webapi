from flask import Flask, jsonify
from flask_restful import Resource
from ormWP import Adm1
import json

class AdministrativeLevel1(Resource):

    def __init__(self):
        super().__init__()

    def get(self):
        """
        Get all Administrative levels 1 from database (zone)
        ---
        description: Query the information of all administrative levels 1 and the API will respond with the list of all regions, this endpoint has no parameters.
        tags:
          - Administrative levels
        responses:
          200:
            description: Administrative level 1
            
            schema:
              id: Adm1
              properties:
                id:
                  type: string
                  description: Id Administrative level 1
                name:
                  type: string
                  description: Administrative level 1 name
                ext_id:
                  type: string
                  description: Extern Id to identify Administrative level 1
        """
        q_set = None
        q_set = Adm1.objects(trace__enabled=True)
        json_data = [{"id":str(x.id),"name":x.name,"ext_id":x.ext_id} for x in q_set]
        return json_data



