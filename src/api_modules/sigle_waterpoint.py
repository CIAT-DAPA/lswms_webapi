from flask import Flask, jsonify
from flask_restful import Resource
from ormWP import Waterpoint
from ormWP import Watershed
from ormWP import Adm3
from ormWP import Adm2
from ormWP import Adm1
import json

class SingleWaterpoints(Resource):

    def __init__(self):
        super().__init__()

    def get(self,waterpoint=None):
        """
        Get all one waterpoint from database 
        ---
        description: Query the information of the ons specific waterpoint. This endpoint needs one parameter, **waterpoint** that is id of the waterpoint to be queried (this id can be obtained from the endpoint `/waterpoints`); The API will respond with the waterpoit with the id provided.
        tags:
          - Waterpoint information
        parameters:
          - in: path
            name: waterpoint
            type: string
            required: true
            description: waterpoint id to be query, for example 64d1bf1cc703fe54e05ee7d6
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
            q_set = Waterpoint.objects(trace__enabled=True)
        else:
            print(waterpoint)
            q_set = Waterpoint.objects(id = waterpoint)
            json_data = []
        for x in q_set:
            watershed_id = str(x.watershed.id)
            
            watershed_info = Watershed.objects(id= watershed_id)
            adm3=Adm3.objects(id= watershed_info[0].adm3.id)
            adm2=Adm2.objects(id= adm3[0].adm2.id)
            adm1=Adm1.objects(id= adm2[0].adm1.id)

            print(adm3[0].name)
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
                    "climatology": x.climatology,
                    "aclimate_id": x.aclimate_id
                }
            json_data.append(json_item)
            

        return json_data