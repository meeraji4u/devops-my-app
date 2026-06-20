pipeline {
    agent any

    options {
        timeout(time: 15, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }

    environment {
        IMAGE_NAME     = 'devops-my-app'
        CONTAINER_NAME = 'devops-my-app-demo'
        APP_PORT       = '5050'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Test') {
            steps {
                echo 'Running container tests...'
                sh '''
                    docker run -d --rm --name test-${BUILD_NUMBER} -p 5051:5000 ${IMAGE_NAME}:${BUILD_NUMBER}
                    sleep 4
                    curl -f http://localhost:5051/health
                    curl -f http://localhost:5051/version
                    docker stop test-${BUILD_NUMBER}
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying container...'
                sh '''
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:5000 ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                echo 'Verifying live deployment...'
                sh '''
                    sleep 3
                    curl -f http://localhost:${APP_PORT}/health
                    echo "Deployment verified successfully"
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline SUCCESS - Build #${BUILD_NUMBER} deployed"
        }
        failure {
            echo 'Pipeline FAILED - check logs above'
        }
        always {
            sh 'docker image prune -f || true'
        }
    }
}
