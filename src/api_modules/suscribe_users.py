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
            if userId == "" or boletin == "" or waterpoint == "":
                return ({"error": "UserId, Boletin and Waterpoint are required"}), 400
            if boletin!="alert" and boletin!="weekly" :
                return ({"error": "Boletin must be alert or weekly"}), 400
            else:
                boletin = Boletin(boletin)
            suscription= Suscription.objects(userId=userId, boletin=boletin).first()
            if suscription:
                print(suscription.waterpoint)
                if waterpoint in suscription.waterpoint:
                  return ({"error": "Suscription already exists"}), 400
                else:
                  suscription.waterpoint.append(waterpoint)
                  suscription.update(waterpoint=suscription.waterpoint)
                  return ({"Sucesfully Created ": "userId:"+ userId +" "+"Boletin:"+ str(boletin._value_)+" "+"waterpoint:"+waterpoint}), 201
            else:
                trace={"created": datetime.now(), "updated": datetime.now(), "enabled": True}
                suscription = Suscription(userId=userId, boletin=boletin, waterpoint=[waterpoint],trace=trace)
                suscription.save()
                return ({"Sucesfully Created ": "userId:"+ userId +" "+"Boletin:"+ str(boletin._value_)+" "+"waterpoint:"+waterpoint}), 201

        except Exception as e:
            return ({"error": str(e)}), 500

class SusbcribeByUserId(Resource):

    def __init__(self):
        super().__init__()

    def get(self, userId=None):
        """
        Get all User Suscriptions
        ---
        description: Get all User Suscriptions
        tags:
          - Users
        parameters:
          - in: path
            name: userId
            type: string
            required: true
            description: userId to be query, for example 64d1be9c16bfd546aec4f58b

        responses:
          200:
            description: All User Suscriptions
          404:
            description: No User Suscriptions found
        """
        try:
            print(userId)
            q_set = None
            if userId is None:
                q_set = Suscription.objects()
            else:
                q_set = Suscription.objects(userId=userId,trace__enabled=True)
            
            json_data = [{"user_id":str(x.userId),"id": str(x.id), "boletin": str(x.boletin._value_), "waterpoint": x.waterpoint} for x in q_set]
            
            return json_data

        except Exception as e:
            return {"error": str(e)}, 500

class SusbcribeBywaterpointId(Resource):

    def __init__(self):
        super().__init__()

    def get(self, waterpointId=None, userId=None):
        """
        Get all waterpoint Suscriptions
        ---
        description: Get all User Suscriptions by waterpoint
        tags:
          - Users
        parameters:
          - in: path
            name: waterpointId
            type: string
            required: true
            description: waterpointId to be query, for example 64d1be9c16bfd546aec4f58b
          - in: path
            name: userId
            type: string
            required: true
            description: userId to be query, for example 64d1be9c16bfd546aec4f58b

        responses:
          200:
            description: All User Suscriptions
          404:
            description: No User Suscriptions found
        """
        try:
            q_set = None

            if waterpointId is not None:
                q_set = Suscription.objects(userId=str(userId),trace__enabled=True)
                q_set = [subscription for subscription in q_set if str(waterpointId) in subscription.waterpoint]
            else:
                return {"error": "No waterpointId"}, 400
            json_data = [{"user_id": str(x.userId), "id": str(x.id), "boletin": str(x.boletin._value_),
                          "waterpoint": str(waterpointId)} for x in q_set]

            return json_data

        except Exception as e:
            return {"error": str(e)}, 500

class Unsuscribeusers(Resource):

    def __init__(self):
        super().__init__()

    def patch(self, waterpointId=None, suscriptionid=None):
        """
        Unsiscibe a user from a waterpoint
        ---
        description: unsiscibe a user from a waterpoint
        tags:
          - Users
        parameters:
          - in: path
            name: waterpointId
            type: string
            required: true
            description: waterpointId to be query, for example 64d1be9c16bfd546aec4f58b
          - in: path
            name: suscriptionid
            type: string
            required: true
            description: suscriptionid to be query, for example 64d1be9c16bfd546aec4f58b

        responses:
          200:
            description: User Unsuscribed
          404:
            description: No User Suscriptions found
        """
        try:
            if suscriptionid is not None:
                q_set = Suscription.objects(id=str(suscriptionid),trace__enabled=True).first()

                if q_set is not None:
                    if str(waterpointId) in q_set.waterpoint:
                        q_set.waterpoint.remove(str(waterpointId))
                        trace=q_set.trace
                        trace['updated']=datetime.now()
                        q_set.update(waterpoint=q_set.waterpoint,trace=trace)

                        if not q_set.waterpoint:
                            trace=q_set.trace
                            trace['enabled']=False
                            q_set.update(trace=trace)
                        return {"message": "sucesfully unsuscribed to waterpoint with the id: "+ waterpointId}
                    else:
                        return {"error": "Waterpoint not found in subscription"}, 404
                else:
                    return {"error": "Subscription not found"}, 404
            else:
                return {"error": "No suscriptionid provided"}, 400

        except Exception as e:
            return {"error": str(e)}, 500
