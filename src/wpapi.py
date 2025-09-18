
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
from api_modules.suscribe_users import SuscribeUsers, SubscribeByUserId,SusbcribeBywaterpointId,Unsuscribeusers
from api_modules.dialy_update import ProtectedEndpoint
from api_modules.woreda import GetWoreda
from api_modules.mean import GetMean
from api_modules.trend import GetTrend
from api_modules.forecast import GetForecast
from api_modules.trend_update import TrendUpdate
from api_modules.forecast_update import ForecastUpdate
from api_modules.last_monitored_by_date import LastMonitoredDataByDate

from api_modules.advisory import AdvisoryEndpoint
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
api.add_resource(SuscribeUsers, '/api/v1/subscribe')

api.add_resource(SubscribeByUserId, '/api/v1/subscribe/get_subscription_by_user/<userId>')
api.add_resource(SusbcribeBywaterpointId, '/api/v1/subscribe/get_subscription_by_waterpoint/<waterpointId>/<userId>')
api.add_resource(Unsuscribeusers, '/api/v1/subscribe/unsubscribe/<waterpointId>/<subscriptionid>')
api.add_resource(ProtectedEndpoint, '/api/v1/monitored/dialy_update')

api.add_resource(AdvisoryEndpoint, '/api/v1/advisory')

# Endpoint for Woreda
api.add_resource(GetWoreda, '/api/v1/woredas')

# Endpoint for Biomass Mean
api.add_resource(GetMean, '/api/v1/biomass_mean')

# Endpoint for Biomass Trend 
api.add_resource(GetTrend, '/api/v1/biomass_trend')

# Endpoint for Biomass Trend Update
api.add_resource(TrendUpdate, '/api/v1/biomass_trend/update')

# Endpoint for Biomass Forecast
api.add_resource(GetForecast, '/api/v1/biomass_forecast')

# Endpoint for Forecast Trend Update
api.add_resource(ForecastUpdate, '/api/v1/biomass_forecast/update')

# Endpoint for Last Monitored Data by Date
api.add_resource(LastMonitoredDataByDate, '/api/v1/lastmonitoredbydate/<date>')



if __name__ == '__main__':
   
    connect(host=config['CONNECTION_DB'])
    print("Connected DB")
    
    if config['DEBUG']:
        app.run(threaded=True, port=config['PORT'], debug=config['DEBUG'])
    else:
        app.run(host=config['HOST'], port=config['PORT'], debug=config['DEBUG'])
