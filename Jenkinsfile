pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'flaskapp'
        DOCKER_IMAGE_NAME = 'yulianbortsov/flask_docker'
        DOCKERHUB_CREDENTIALS_ID = 'c18e7966-672e-48de-baf9-673a8ae98fe0'
        EC2_HOST = '44.212.65.210'
        EC2_USER = 'ec2-user'
        SSH_KEY_CREDENTIALS_ID = '2b5a27f6-928a-4673-aa89-6d484b86cf65'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/YulianBortsov/learn_flask_docker.git', branch: 'main'
            }
        }

        stage('Build and Run Containers') {
            steps {
                script {
                    sh 'docker-compose down --remove-orphans'
                    sh 'docker-compose build'
                    sh 'docker-compose up -d'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    sh '''
                    sleep 10  # wait for the app to start
                    curl -f http://localhost:5000/hello || exit 1
                    '''
                }
            }
        }

        stage('Process Test Results') {
            steps {
                script {
                    def result = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:5000/hello", returnStdout: true).trim()
                    if (result == '200') {
                        echo 'Test passed. Server responded with HTTP 200.'
                    } else {
                        echo "Test failed. Server responded with HTTP ${result}."
                        error 'Stopping the pipeline due to failed tests.'
                    }
                }
            }
        }
        
        stage('Modify docker-compose.yml') {
            steps {
                script {
                    // Update the docker-compose.yml to use the pre-built image for Flask app
                    sh '''
                    sed -i 's|build: .|image: ${DOCKER_IMAGE_NAME}:latest|' docker-compose.yml
                    sed -i 's|command: flask run --host=0.0.0.0|command: flask run --host=0.0.0.0|' docker-compose.yml
                    # Remove the volume mount for init.sql if not needed
                    sed -i '/init.sql/d' docker-compose.yml
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'c18e7966-672e-48de-baf9-673a8ae98fe0') {
                        def appImage = docker.build("${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}")
                        appImage.push()
                        appImage.push("latest")
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    sshagent([SSH_KEY_CREDENTIALS_ID]) {
                       sh '''
                            scp -o StrictHostKeyChecking=no docker-compose.yml ${EC2_USER}@${EC2_HOST}:/home/${EC2_USER}/docker-compose/
                            ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} << 'EOF'
                                cd /home/${EC2_USER}/docker-compose/
                                docker-compose down -v
                                docker-compose pull
                                docker-compose up -d
                            EOF
                        '''
                    }
                }
            }
        }
        stage('Cleanup') {
            steps {
                script {
                    sh 'docker-compose down'
                    // Run the cleanup script
                    sh './remove_old_images.sh'
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning workspace...'
            cleanWs()
        }
    }
}

