from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from ormWP import Suscription,Boletin
from datetime import datetime
import json


class SuscribeUsers(Resource):

    def __init__(self):
        super().__init__()

    def post(self):
        """
        Create a new User Suscription entry
        ---
        description: Create a new User Suscription entry
        tags:
          - Users
        parameters:
          - in: body
            name: body
            required: true
            schema:
              id: Suscription
              properties:
                userId:
                  type: string
                  description: Id of the User
                boletin:
                  type: string
                  description: Boletin to suscribe
                waterpoint:
                  type: string
                  description: id to waterpoint to suscribe              
        responses:
          201:
            description: Suscription created successfully
          400:
            description: Bad Request, invalid input data
        """
        try:
            data = request.get_json()
            userId = data.get('userId')
            boletin = data.get('boletin')
            waterpoint = data.get('waterpoint')
            boletin = data.get('boletin', None)
            print(data)
            if boletin!="alert" and boletin!="weekly" :
                return ({"error": "Boletin must be alert or weekly"}), 400
            else:
                boletin = Boletin(boletin)
                print(boletin)
            suscription= Suscription.objects(userId=userId, boletin=boletin, waterpoint=waterpoint).first()
            if suscription is not None:
                return ({"error": "Suscription already exists"}), 400
            if userId is "" or boletin is "" or waterpoint is "":
                return ({"error": "UserId, Boletin and Waterpoint are required"}), 400
            trace={"created": datetime.now(), "updated": datetime.now(), "enabled": True}
            suscription = Suscription(userId=userId, boletin=boletin, waterpoint=waterpoint,trace=trace)	
            #print("UserId: ", str(userId), "Boletin: ", str(Boletin), "Waterpoint: ", str(Waterpoint))
            suscription.save()
            return ({"Sucesfully": "created"+ " "+ userId +" "+ str(boletin._value_)+" "}), 201

        except Exception as e:
            return ({"error": str(e)}), 500


