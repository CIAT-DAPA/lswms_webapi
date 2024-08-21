# import os
# from flask_restful import Resource
# from URLSearchParams import URLSearchParams
# import requests
# from flask import Flask, jsonify, request

# import json
# import ast

# GEOSERVER_URL="https://geo.aclimate.org/geoserver/waterpoints_et/"
# SERVICEE="wms"

# class Coordinates(Resource):

#     def __init__(self):
#         super().__init__()

#     def post(self):
#         """
#         Get Features, Information of Biomas.
        
#         ---

#         tags:
#           - Coordinates
#         parameters:
#           - in: body
#             name: body
#             required: true
#             description: "Data required to retrieve geospatial features at a specific point, for a specific date, from a specific layer, on the geospatial server this endppoint needs three data in the body, **layer** that is the name of the layer on the geospatial server, **coor** that is a list of objects containing coordinates (latitude and longitude) of the points, and **date** that is the date for which the information is desired."
#             schema:
#               type: object
#               properties:
#                 layer:
#                   type: string
#                   example: "biomass"
#                   description: "Name of the layer on the geospatial server."
#                 coor:
#                   type: array
#                   items:
#                     type: object
#                     properties:
#                       lat:
#                         type: number
#                         description: "Latitude of the point."
#                       lon:
#                         type: number
#                         description: "Longitude of the point."
#                   description: "List of objects containing coordinates (latitude and longitude) of the points."
#                 date:
#                   type: string
#                   example: "2023-01-17"
#                   description: "Date for which the information is desired."
#         responses:
#           200:
#             description: layer, latitude, longitude, value and date
#             schema:
#               id: Features
#               properties:
#                 layer:
#                   type: string
#                   format: string
#                   description: layer of geoserver
#                   example: biomass
#                 date:
#                   type: string
#                   format: string 
#                   description: date in which you want to extract the information from the mosaic
#                   example: 2023-01-17	
#                 lat:
#                   type: number
#                   format: float
#                   description: lat
#                   example: 7.17712
#                 lon:
#                   type: number
#                   format: float
#                   description: lat
#                   example: 8.5583
#                 value:
#                   type: number
#                   format: float
#                   description: values
#                   example: 20.00
#         """
#         data = request.get_json()

#         layer = data.get('layer')
#         coor = data.get('coor')
#         date = data.get('date')

#         if not layer or not coor or not date:
#             return {"error": "Missing required parameters"}, 400

#         result_list = []

#         for i in coor:
#             lat = i['lat']
#             lon = i['lon']
#             parameters = {
#                 'service': 'WMS',
#                 'version': '1.1.1',
#                 'request': 'GetFeatureInfo',
#                 'time': date,
#                 'layers': layer,
#                 'query_layers': layer,
#                 'feature_count': 50,
#                 'info_format': 'application/json',
#                 'format_options': 'callback:handleJson',
#                 'SrsName': 'EPSG:404000',
#                 'width': 101,
#                 'height': 101,
#                 'x': 50,
#                 'y': 50,
#                 'bbox': str(lon - 0.1) + ',' + str(lat - 0.1) + ',' + str(lon + 0.1) + ',' + str(lat + 0.1)
#             }

#             url = str(URLSearchParams(GEOSERVER_URL + SERVICEE).append(parameters))
#             print(url)
#             response = requests.get(url)
#             data = response.json()

#             if 'features' in data and data['features']:
#                 gray_index = data['features'][0]['properties'].get('GRAY_INDEX')
#                 if gray_index is not None:
#                     response_data = {'layer': layer, 'lat': lat, 'lon': lon, 'value': gray_index, 'date': date}
#                     if response_data not in result_list:
#                         result_list.append(response_data)

#         return result_list, 200
