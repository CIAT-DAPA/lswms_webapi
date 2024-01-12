from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from ormWP import Adm1
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
                UserId:
                  type: string
                  description: Id of the User
                Boletin:
                  type: string
                  description: Boletin to suscribe
                Waterpoint:
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
            userId = data.get('UserId')
            Boletin = data.get('Boletin')
            Waterpoint = data.get('Waterpoint')
            print(data)
            if userId is None or Boletin is None or Waterpoint is None:
                return ({"error": "UserId, Boletin and Waterpoint are required"}), 400

            #print("UserId: ", str(userId), "Boletin: ", str(Boletin), "Waterpoint: ", str(Waterpoint))

            return ({"Sucesfully": "created"+ " "+ userId +" "+ Boletin+" "}), 201

        except Exception as e:
            return ({"error": str(e)}), 500


