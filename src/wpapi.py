
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
from api_modules.watershed import Watersheds
from api_modules.waterpoint import Waterpoints
from api_modules.sigle_waterpoint import SingleWaterpoints
from api_modules.monitored_data import MonitoredData
from api_modules.warterpoint_profile import WaterpointsProfile
from api_modules.single_waterpoint_profile import SingleWaterpointsProfile

#from api_modules.layers import Layers


app = Flask(__name__)
CORS(app)
api = Api(app)
swagger = Swagger(app)


@app.route('/')
def home():
    return redirect("/apidocs")



api.add_resource(AdministrativeLevel1, '/api/v1/adm1')
api.add_resource(AdministrativeLevel2, '/api/v1/adm2/<adm1>')
api.add_resource(AdministrativeLevel3, '/api/v1/adm3/<adm2>')
api.add_resource(Watersheds, '/api/v1/watershed/<adm3>')
api.add_resource(Waterpoints, '/api/v1/waterpoints')
api.add_resource(SingleWaterpoints, '/api/v1/waterpoints/<waterpoint>')
api.add_resource(MonitoredData, '/api/v1/monitored/<waterpoint>')
api.add_resource(WaterpointsProfile, '/api/v1/waterpointsprofiles')
api.add_resource(SingleWaterpointsProfile, '/api/v1/waterpointsprofiles/<waterpoint>')






if __name__ == '__main__':
    connect(host=config['CONNECTION_DB'])
    print("Connected DB")
    
    if config['DEBUG']:
        app.run(threaded=True, port=config['PORT'], debug=config['DEBUG'])
    else:
        app.run(host=config['HOST'], port=config['PORT'],
                debug=config['DEBUG'])

