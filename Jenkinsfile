// Define an empty map for storing remote SSH connection parameters
def remote = [:]

pipeline {

    agent any

    environment {
        user = credentials('wp_user')
        host = credentials('wp_host')
        name = credentials('wp_name')
        ssh_key = credentials('wp_devops')
    }

    stages {
        stage('Ssh to connect Bigelow server') {
            steps {
                script {
                    // Set up remote SSH connection parameters
                    remote.allowAnyHosts = true
                    remote.identityFile = ssh_key
                    remote.user = user
                    remote.name = name
                    remote.host = host
                    
                }
            }
        }
        stage('Download latest release') {
            steps {
                script {
                    sshCommand remote: remote, command: """
                        cd /var/www/waterpointsapi/
                        mkdir prueba
                        rm -rf prueba
                    """
                }
            }
        }
        /* stage('Init Api') {
            steps {
                script {
                    sshCommand remote: remote, command: """
                        cd /var/www/waterpointsapi/
                        export DEBUG=False
                        export PORT=5000
                        export CONNECTION_DB=mongodb://localhost:27017/waterpoints
                        export HOST=0.0.0.0
                        cd api/
                        nohup python wpapi.py > log.txt 2>&1 &
                    """
                }
            }
        } */
    }
    
    post {
        failure {
            script {
                echo 'fail'
            }
        }

        success {
            script {
                echo 'everything went very well!!'
            }
        }
    }
 
}