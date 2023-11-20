from flask import Flask, jsonify
from flask_restful import Resource
from ormWP import Monitored, Wpcontent,Wscontent,Waterpoint,Watershed
import json

class LastMonitoredData(Resource):
    def __init__(self):
        super().__init__()

    def get(self, waterpoint=None):
        """
        Get last Monitored data
        ---
        description: Query the information of last monitored data from one waterpoint . This endpoint needs one parameter, **waterpoint** that is id of the waterpoint to be queried (this id can be obtained from the endpoint `/waterpoint`); The API will respond with the list of the last monitored values from that specific waterpoint.
        tags:
          - Waterpoint Monitored data
        parameters:
          - in: path
            name: waterpoint
            type: string
            required: true
            description: waterpoint id to be query, for example 64d1bf1cc703fe54e05ee7d6
        responses:
          200:
            description: Monitored data
            schema:
              id: Monitored
              properties:
                id:
                  type: string
                  description: Id Monitored data
                date:
                  type: string
                  description: Date of the monitored data
                values:
                  type: array
                  items: {}
                  description: List of values of the monitored data
                waterpoint:
                  type: string
                  description: Id waterpoint
                
        """
        
        En=False
        Am=False
        Or=False
        if waterpoint is None:
            q_set = Monitored.objects()
        else:
            q_set = Monitored.objects(waterpoint=waterpoint).order_by('-date').limit(1)
            q_setWpC=Wpcontent.objects(waterpoint=waterpoint)
            water=Waterpoint.objects(id=waterpoint).first()
            q_setWsC=Wscontent.objects(watershed=water.watershed.id)
            
        for wsc in q_setWsC:
            if(wsc.content['language']=='en'):
                En=True
            elif (wsc.content['language']=='or'):
                Or=True
            elif (wsc.content['language']=='am'):
                Am=True
            
        for wpc in q_setWpC:
            if(wpc.content['language']=='en'):
                En=True
            elif (wpc.content['language']=='or'):
                Or=True
            elif (wpc.content['language']=='am'):
                Am=True
        json_data = [{"id": str(x.id), "date": x.date.isoformat(), "values": x.values, "waterpointId": waterpoint,"am":Am,"en":En,"or":Or} for x in q_set]

        return json_data
