import os 

config = {}

if os.getenv('DEBUG', "true").lower() == "true":
    config['DEBUG'] = True
    config['HOST'] = 'localhost'
    config['PORT'] = 5001
    config['CONNECTION_DB']='mongodb://root:s3cr3t@localhost:27017/waterpoints?authSource=admin'
else:
    config['DEBUG'] = False
    config['HOST'] = '0.0.0.0'
    config['PORT'] = os.getenv('API_SPCAT_PORT')
    config['CONNECTION_DB']=os.getenv('CONNECTION_DB')

    