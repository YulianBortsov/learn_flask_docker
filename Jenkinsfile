pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'flaskapp'
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

