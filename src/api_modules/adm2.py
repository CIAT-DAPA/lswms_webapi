from flask import Flask, jsonify
from flask_restful import Resource
from ormWP import Adm2
import json

class AdministrativeLevel2(Resource):

    def __init__(self):
        super().__init__()

    def get(self, adm1 = None):
        """
        Get all Administrative levels 2 from database (woreda)
        ---
        description: Query the information of the administrative levels 2 (woreda). This endpoint needs one parameter, **adm1** that is id of the administrative levels 1 (zone) to be queried (this id can be obtained from the endpoint `/adm1`); The API will respond with the list of the woredas from that specific zone.
        tags:
          - Administrative levels
        parameters:
          - in: path
            name: adm1
            type: string
            required: true
            description: adm1 id to be query, for example 64d1be9c16bfd546aec4f58b
        responses:
          200:
            description: Administrative levels 2
            schema:
              id: Adm2
              properties:
                id:
                  type: string
                  description: Id Administrative level 2
                name:
                  type: string
                  description: Administrative level 2 name
                ext_id:
                  type: string
                  description: Extern Id to identify Administrative level 2
                adm1:
                  type: string
                  description: Id Administrative level 1
        """
        q_set = None
        if adm1 is None:
            q_set = Adm2.objects(trace__enabled=True)
        else:
            q_set = Adm2.objects(adm1=adm1)
        json_data = [{"id":str(x.id),"name":x.name,"ext_id":x.ext_id,"adm1":str(x.adm1.id)} for x in q_set]
        return json_data
