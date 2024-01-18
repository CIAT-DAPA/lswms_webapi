from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from ormWP import Suscription,Boletin,Waterpoint,Watershed,Adm1,Adm2,Adm3,Monitored
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
                  description: Boletin to subscribe
                waterpoint:
                  type: string
                  description: id to waterpoint to subscribe              
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
            suscription= Suscription.objects(userId=userId, boletin=boletin,trace__enabled=True).first()
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

class SubscribeByUserId(Resource):

    def __init__(self):
        super().__init__()

    def get(self, userId=None):
        """
        Get all User Subscriptions
        ---
        description: Get all User Subscriptions
        tags:
          - Users
        parameters:
          - in: path
            name: userId
            type: string
            required: true
            description: userId to be queried, for example, 64d1be9c16bfd546aec4f58b

        responses:
          200:
            description: All User Subscriptions
          404:
            description: No User Subscriptions found
        """
        try:
            print(userId)
            q_set = None
            if userId is None:
                q_set = Suscription.objects()
            else:
                q_set = Suscription.objects(userId=userId, trace__enabled=True)
            
            json_data = []
            
            for x in q_set:
                waterpoint_info_list = Waterpoint.objects(id__in=x.waterpoint).all()
                
                waterpoint_data = []
                for waterpoint_info in waterpoint_info_list:
                    watershed_info = Watershed.objects(id=waterpoint_info.watershed.id).first()
                    adm3=Adm3.objects(id=watershed_info.adm3.id).first()
                    adm2=Adm2.objects(id=adm3.adm2.id).first()
                    adm1=Adm1.objects(id=adm2.adm1.id).first()
                    last__monitored = Monitored.objects(waterpoint=waterpoint_info.id).order_by('-date').limit(1)

                    waterpoint_data.append({
                        "id": str(waterpoint_info.id),
                        "waterpoint_name": str(waterpoint_info.name),
                        "adm3_name": str(adm3.name),
                        "adm2_name": str(adm2.name),
                        "adm1_name": str(adm1.name),
                        "last_monitored_deph": float(last__monitored[0].values[0]["value"]) if last__monitored else None, 
                        "last_monitored_scaled_depth": float(last__monitored[0].values[3]["value"]) if last__monitored else None                      

                    })

                data = {
                    "user_id": str(x.userId),
                    "id": str(x.id),
                    "boletin": str(x.boletin._value_),
                    "waterpoints": waterpoint_data
                }
                json_data.append(data)
            
            return json_data

        except Exception as e:
            return {"error": str(e)}, 500

class SusbcribeBywaterpointId(Resource):

    def __init__(self):
        super().__init__()

    def get(self, waterpointId=None, userId=None):
        """
        Get all waterpoint Subscriptions by user and waterpoint
        ---
        description: Get all User Subscriptions by user and waterpoint
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
            description: All User Subscriptions
          404:
            description: No User Subscriptions found
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

    def patch(self, waterpointId=None, subscriptionid=None):
        """
        Unsubscribe a user from a waterpoint
        ---
        description: Unsubscribe a user from a waterpoint
        tags:
          - Users
        parameters:
          - in: path
            name: waterpointId
            type: string
            required: true
            description: waterpointId to be query, for example 64d1be9c16bfd546aec4f58b
          - in: path
            name: subscriptionid
            type: string
            required: true
            description: subscription id to be query, for example 64d1be9c16bfd546aec4f58b

        responses:
          200:
            description: User Unsuscribed
          404:
            description: No User Suscriptions found
        """
        try:
            if subscriptionid is not None:
                q_set = Suscription.objects(id=str(subscriptionid),trace__enabled=True).first()

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
