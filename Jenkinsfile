// Define an empty map for storing remote SSH connection parameters
def remote = [:]

pipeline {

    agent any

    environment {
        server_name = credentials('wp_name')
        server_host = credentials('wp_host')
        ssh_key = credentials('wp_devops')
    }

    stages {
        stage('Ssh to connect bigelow server') {
            steps {
                script {
                    // Set up remote SSH connection parameters
                    remote.allowAnyHosts = true
                    remote.identityFile = ssh_key
                    remote.user = ssh_key_USR
                    remote.name = server_name
                    remote.host = server_host
                    
                }
            }
        }
        stage('Download latest release and create enviroment') {
            steps {
                script {
                    sshCommand remote: remote, command: """
                        cd /var/www/waterpointsApi
                        if [ ! -d api_WP ]; then
                            mkdir ./api_WP
                        fi
                        cd /var/www/waterpointsApi/api_WP
                        rm -rf env
                        rm -rf src
                        sudo kill -9 \$(sudo ss -nepal | grep 5000 | awk '{print \$9}' | awk -F '/' '{print \$1}')
                        curl -LOk https://github.com/CIAT-DAPA/lswms_webapi/releases/latest/download/releaseApi.zip
                        unzip -o releaseApi.zip
                        rm -fr releaseApi.zip
                        python3 -m venv env
                    """
                }
            }
        }
        stage(' activate enviroment and install requirements') {
            steps {
                script {
                    sshCommand remote: remote, command: """
                        cd /var/www/waterpointsApi/api_WP
                        source env/bin/activate
                        cd src
                        pip install -r requirements.txt
                    """
                }
            }
        }
        stage('Init api') {
            steps {
                script {
                    sshCommand remote: remote, command: """
                        cd /var/www/waterpointsApi/api_WP
                        source env/bin/activate
                        cd src
                        export DEBUG=False
                        export API_WP_PORT=5001
                        export CONNECTION_DB=mongodb://localhost:27017/waterpoints
                        export HOST=0.0.0.0
                        nohup python3 wpapi.py > log.txt 2>&1 &
                    """
                }
            }
        }       
    }
    
    post {
        failure {
            script {
                echo 'fail'
            }
        }

        success {
            script {
                echo 'everything went very well, api in production'
            }
        }
    }
 
}
