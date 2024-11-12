from flask import jsonify, make_response
from flask_restful import Resource
from ormWP import Woreda

class GetWoreda(Resource):
    def __init__(self):
        super().__init__()

    def get(self):
        """
        Get all Woredas from the database covering the area of interest.
        ---
        description: Query the information of all Woredas. The API will respond with a list of all Woredas that are currently enabled. This endpoint has no parameters.
        tags:
          - Biomass
        responses:
          200:
            description: Woreda list
            schema:
              id: Woreda
              properties:
                id:
                  type: string
                  description: Id of the Woreda
                name:
                  type: string
                  description: Woreda Name
                ext_id:
                  type: string
                  description: External Id to identify the Woreda
          500:
            description: Server error
        """
        try:
            # Query the database for enabled Woredas
            q_set = Woreda.objects(trace__enabled=True)

            # Convert to JSON response
            json_data = [{"id": str(x.id), "name": x.name, "ext_id": x.ext_id} for x in q_set]
            
            return make_response(jsonify(json_data), 200)
        
        except Exception as e:
            # Log the error and return an internal server error response
            error_message = {"error": "An error occurred while fetching the Woreda data.", "details": str(e)}
            return make_response(jsonify(error_message), 500)
