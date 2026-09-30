pipeline {

    agent any

    environment {
        PYTHON = 'C:\\Program Files\\Python312\\python.exe'
        IMAGE_NAME = "customer-portal:build-${BUILD_NUMBER}"
        CONTAINER_NAME = "customer-portal-${BUILD_NUMBER}"
        HOST_PORT = "5001"
        CONTAINER_PORT = "5000"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub'

                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/kaushiksha23/customer-portal.git',
                        credentialsId: 'github-credentials'
                    ]]
                ])
            }
        }

        stage('Build') {
            steps {
                echo 'Installing Python dependencies'

                bat "\"${PYTHON}\" -m pip install -r requirements.txt"

                echo 'Building Python application'

                bat "\"${PYTHON}\" -m compileall app.py test_app.py"
            }
        }

        stage('Test') {
            steps {
                echo 'Running automated tests'

                bat "\"${PYTHON}\" -m pytest -v"
            }
        }

        stage('Docker Build') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}"

                bat "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Container Verification') {
            steps {
                echo "Starting temporary container: ${CONTAINER_NAME}"

                bat "docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${CONTAINER_PORT} ${IMAGE_NAME}"

                echo 'Waiting for application to start'

                bat 'powershell -Command "Start-Sleep -Seconds 5"'

                echo 'Checking application health endpoint'

                bat 'powershell -Command "Invoke-WebRequest -Uri http://localhost:%HOST_PORT%/health -UseBasicParsing"'

                echo 'Container verification successful'
            }
        }

        stage('Cleanup') {
            steps {
                echo "Cleaning up temporary container: ${CONTAINER_NAME}"

                bat "docker rm -f ${CONTAINER_NAME} 2>NUL || exit /b 0"
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed'
        }
    }
}