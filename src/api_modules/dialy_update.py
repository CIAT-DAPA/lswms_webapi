from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd


API_KEY = "tu_clave_secreta"

class ProtectedEndpoint(Resource):
    def __init__(self):
        super().__init__()

    def post(self):
        """
        Procesar un DataFrame protegido por una clave de autenticación.

        ---
        tags:
          - DataFrame
        parameters:
          - in: header
            name: Authorization
            type: string
            required: true
            description: Clave de autenticación en el formato "Bearer tu_clave_secreta"
          - in: body
            name: dataframe
            description: DataFrame en formato JSON
            required: true
            schema:
              type: object
              example: {"col1": [1, 2, 3], "col2": ["A", "B", "C"]}

        responses:
          200:
            description: DataFrame recibido y procesado con éxito
          401:
            description: Unauthorized - Clave de autenticación inválida o faltante
          500:
            description: Error interno del servidor al procesar el DataFrame
        """
        try:
            # Verificar la autenticación mediante la clave en el header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return {"error": "Unauthorized"}, 401

            received_api_key = auth_header.split(" ")[1]
            if received_api_key != API_KEY:
                return {"error": "Invalid API key"}, 401

            # Si la autenticación es exitosa, procesar el DataFrame
            data = request.get_json()
            df = pd.DataFrame(data)
            print(df)
            # Aquí puedes realizar las operaciones que necesites con el DataFrame df
            # ...

            return {"message": "DataFrame received and processed successfully"}

        except Exception as e:
            return {"error": str(e)}, 500

