
import os
import sys
from flask import Flask, redirect
from flask_restful import Api
from flask_cors import CORS
from flasgger import Swagger
from conf import config

#from api_modules.clipping_raster import ClippingRaster
# New Modules
from mongoengine import *
from api_modules.adm1 import AdministrativeLevel1
from api_modules.adm2 import AdministrativeLevel2
from api_modules.adm3 import AdministrativeLevel3
from api_modules.waterpoint import Waterpoints
from api_modules.sigle_waterpoint import SingleWaterpoints
from api_modules.monitored_data import MonitoredData
from api_modules.waterpoint_profiles import SingleWaterpointsProfile
from api_modules.monitored_latest  import LastMonitoredData
from api_modules.suscribe_users import SuscribeUsers, SusbcribeByUserId,SusbcribeBywaterpointId,Unsuscribeusers
#from api_modules.layers import Layers

 
app = Flask(__name__)
CORS(app)
api = Api(app)
swagger = Swagger(app)

# Define tus endpoints en el orden deseado

@app.route('/')
def home():
    return redirect("/apidocs")

# Endpoint para AdministrativeLevel1
api.add_resource(AdministrativeLevel1, '/api/v1/adm1')

# Endpoint para AdministrativeLevel2
api.add_resource(AdministrativeLevel2, '/api/v1/adm2/<adm1>')

# Endpoint para AdministrativeLevel3
api.add_resource(AdministrativeLevel3, '/api/v1/adm3/<adm2>')

# Endpoint para Waterpoints
api.add_resource(Waterpoints, '/api/v1/waterpoints')

# Endpoint para SingleWaterpoints
api.add_resource(SingleWaterpoints, '/api/v1/waterpoints/<waterpoint>')

# Endpoint para MonitoredData
api.add_resource(MonitoredData, '/api/v1/monitored/<waterpoint>')

# Endpoint para LastMonitoredData
api.add_resource(LastMonitoredData, '/api/v1/lastmonitored/<waterpoint>')

# Endpoint para SingleWaterpointsProfile
api.add_resource(SingleWaterpointsProfile, '/api/v1/waterpointsprofiles/<waterpoints>/<language>')

# Endpoint para SuscribeUsers
api.add_resource(SuscribeUsers, '/api/v1/suscribe')

api.add_resource(SusbcribeByUserId, '/api/v1/suscribe/get_suscription_by_user/<userId>')
api.add_resource(SusbcribeBywaterpointId, '/api/v1/suscribe/get_suscription_by_waterpoint/<waterpointId>/<userId>')
api.add_resource(Unsuscribeusers, '/api/v1/suscribe/unsubscribe/<waterpointId>/<suscriptionid>')
if __name__ == '__main__':
    connect(host=config['CONNECTION_DB'])
    print("Connected DB")
    
    if config['DEBUG']:
        app.run(threaded=True, port=config['PORT'], debug=config['DEBUG'])
    else:
        app.run(host=config['HOST'], port=config['PORT'], debug=config['DEBUG'])
