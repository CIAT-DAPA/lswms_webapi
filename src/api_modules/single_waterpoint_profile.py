from flask import Flask, jsonify
from flask_restful import Resource
from ormWP import Waterpoint
from ormWP import Adm1
from ormWP import Adm2
from ormWP import Adm3
from ormWP import Watershed
from ormWP import Wpcontent
from ormWP import Wscontent


import json

class SingleWaterpointsProfile(Resource):

    def __init__(self):
        super().__init__()

    def get(self, waterpoint=None):
        """
        Get all waterpoints profiles from database 
        ---
        description: Query the information of the one waterpoints profile. This endpoint has not parameter.  This endpoint needs one parameter, **waterpoint** that is id of the waterpoint to be queried (this id can be obtained from the endpoint `/waterpoints`); The API will respond with the waterpoit profile with the id provided.
        parameters:
          - in: path
            name: waterpoint
            type: string
            required: true
        responses:    
          200:
            description: Waterpoints profiles
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
                watershed_name:
                  type: string
                  description: Name of the watershed
                adm3:
                  type: string
                  description: Name of adm3
                adm2:
                  type: string
                  description: Name of adm2
                adm1:
                  type: string
                  description: Name of adm1
                contents_wp:
                  type: array
                  description: List of contents associated with the waterpoint
                  items:
                    type: string
                contents_ws:
                  type: array
                  description: List of contents associated with the watershed
                  items:
                    type: string
        """
        q_set = None
        if waterpoint is None:
            q_set = Waterpoint.objects()
        else:
            print(waterpoint)
            q_set = Waterpoint.objects(id = waterpoint)
        json_data = []

        for waterpoint in q_set:
            watershed_id = str(waterpoint.watershed.id)
            watershed = Watershed.objects(id=watershed_id).first()
            adminlevel3id = watershed.adm3.id
            adm3 = Adm3.objects.get(id=adminlevel3id)
            watershed_name = watershed.name
            adminlevel2id = adm3.adm2.id
            adm2 = Adm2.objects.get(id=adminlevel2id)
            adminlevel1id = adm2.adm1.id
            adm1 = Adm1.objects.get(id=adminlevel1id)

            wp_contents = Wpcontent.objects(waterpoint=str(waterpoint.id))
            ws_contents = Wscontent.objects(watershed=str(waterpoint.watershed.id))
            contents_list = [content.content for content in wp_contents]
            for content in contents_list:
                if 'trace' in content:
                    del content['trace']

            contents_list_ws = [content.content for content in ws_contents]
            for content in contents_list_ws:
                if 'trace' in content:
                    del content['trace']

            waterpoint_data = {
                "id": str(waterpoint.id),
                "name": waterpoint.name,
                "lat": waterpoint.lat,
                "lon": waterpoint.lon,
                "area": waterpoint.area,
                "aclimate_id":waterpoint.aclimate_id,
                "ext_id": str(waterpoint.ext_id),
                "watershed": watershed_id,
                "watershed_name": watershed_name,
                "adm3": adm3.name,
                "adm2": adm2.name,
                "adm1": adm1.name,
                "contents_wp": contents_list,
                "contents_ws": contents_list_ws,

            }

            json_data.append(waterpoint_data)

        return json_data



