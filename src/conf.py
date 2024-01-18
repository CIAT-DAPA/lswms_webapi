import os 

config = {}

if os.getenv('DEBUG', "true").lower() == "true":
    config['API_KEY'] = 'prueba'
    config['DEBUG'] = True
    config['HOST'] = 'localhost'
    config['PORT'] = 5000
    config['CONNECTION_DB']='mongodb://root:s3cr3t@localhost:27017/waterpoints?authSource=admin'
else:
    config['DEBUG'] = False
    config['HOST'] = '0.0.0.0'
    config['PORT'] = os.getenv('API_WP_PORT')
    config['CONNECTION_DB']=os.getenv('CONNECTION_DB')
    config['API_KEY'] = os.getenv('API_KEY')

    