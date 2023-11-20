from flask import Flask, jsonify
from flask_restful import Resource
from ormWP import Waterpoint
from ormWP import Watershed
from ormWP import Adm3
from ormWP import Adm2
from ormWP import Adm1

import json

class Waterpoints(Resource):

    def __init__(self):
        super().__init__()

    def get(self):
        """
        Get all waterpoints  from database 
        ---
        description: Query the information of the waterpoints. This endpoint has not parameter.
        tags:
          - Waterpoint information
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

        json_data = []

        for x in q_set:
            watershed_id = str(x.watershed.id)
            
            watershed_info = Watershed.objects(id= watershed_id)
            adm3=Adm3.objects(id= watershed_info[0].adm3.id)
            adm2=Adm2.objects(id= adm3[0].adm2.id)
            adm1=Adm1.objects(id= adm2[0].adm1.id)

            if watershed_info:
                json_item = {
                    "id": str(x.id),
                    "name": x.name,
                    "lat": x.lat,
                    "lon": x.lon,
                    "area": x.area,
                    "ext_id": str(x.ext_id),
                    "watershed": watershed_id,
                    "watershed_name": watershed_info[0].name,
                    "adm3":adm3[0].name,
                    "adm2":adm2[0].name,
                    "adm1":adm1[0].name,
                    "aclimate_id": x.aclimate_id
                }
            json_data.append(json_item)
        return json_data