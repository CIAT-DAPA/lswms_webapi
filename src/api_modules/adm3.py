from flask import Flask, jsonify
from flask_restful import Resource
from ormWP import Adm3
import json

class AdministrativeLevel3(Resource):

    def __init__(self):
        super().__init__()

    def get(self,adm2=None):
        """
        Get all Administrative levels 3 from database (kebele)
        ---
        description: Query the information of the administrative levels 3 (kebele). This endpoint needs one parameter, **adm2** that is id of the administrative levels 2 (woreda) to be queried (this id can be obtained from the endpoint `/adm2`); The API will respond with the list of the kebeles from that specific woreda.
        tags:
          - Administrative levels
        parameters:
          - in: path
            name: adm2
            type: string
            required: true
            description: adm2 id to be query, for example 64d1bec4f8b9461ac6ed74cb
        responses:    
          200:
            description: Administrative levels 3
            schema:
              id: Adm3
              properties:
                id:
                  type: string
                  description: Id Administrative level 3
                name:
                  type: string
                  description: Administrative level 3 name
                ext_id:
                  type: string
                  description: Extern Id to identify Administrative level 3
                adm2:
                  type: string
                  description: Id Administrative level 2
        """
        q_set = None
        if adm2 is None:
            q_set = Adm3.objects()
        else:
            print(adm2)
            q_set = Adm3.objects(adm2 = adm2)
        json_data = [{"id":str(x.id),"name":x.name,"ext_id":x.ext_id,"adm2":str(x.adm2.id)} for x in q_set]
        return json_data