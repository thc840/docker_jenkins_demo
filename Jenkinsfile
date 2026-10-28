pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'thc480/docker_jenkins_demo'
        CONTAINER_NAME    = 'production_app'
        HOST_PORT         = '8085'
        CONTAINER_PORT    = '5000'
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}..."
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER} -t ${DOCKER_IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    echo "Deploying updated container to port ${HOST_PORT}..."
                    sh """
                        docker rm -f ${CONTAINER_NAME} || true

                        docker run -d \
                            --name ${CONTAINER_NAME} \
                            --restart unless-stopped \
                            -p ${HOST_PORT}:${CONTAINER_PORT} \
                            ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}
                    """
                }
            }
        }

        stage('Verify Health') {
            steps {
                script {
                    echo "Verifying application..."
                    sh """
                        sleep 3
                        STATUS=\$(docker inspect --format='{{.State.Status}}' ${CONTAINER_NAME})
                        echo "Container Status: \$STATUS"

                        if [ "\$STATUS" != "running" ]; then
                            echo "Deployment failed: container crashed on startup."
                            docker logs ${CONTAINER_NAME}
                            exit 1
                        fi

                        curl --fail --retry 3 --retry-delay 2 http://localhost:${HOST_PORT}/ || {
                            echo "Application failed to respond to HTTP requests."
                            docker logs ${CONTAINER_NAME}
                            exit 1
                        }

                        echo "Deployment successful: Application is live on port ${HOST_PORT}."
                    """
                }
            }
        }
    }

    post {
        failure {
            echo "Pipeline failed. Check stage logs for details."
        }
        cleanup {
            sh "docker image prune -f || true"
        }
    }
}
