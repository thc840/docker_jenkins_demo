pipeline {
    agent any

    environment {
        GIT_REPOSITORY_URL = 'https://github.com/thc840/docker_jenkins_demo.git'
        DOCKER_IMAGE_NAME  = 'thc480/docker_jenkins_demo'
        IMAGE_TAG          = '1.1'
        CONTAINER_NAME     = 'docker_jenkins_demo_container'
        HOST_PORT          = '8088'
        CONTAINER_PORT     = '5000'
    }

    stages {
        stage('Clone Repository') {
            steps {
                script {
                    try {
                        git branch: 'jenkin_pipeline_container_run', url: GIT_REPOSITORY_URL
                    } catch (Exception e) {
                        echo "Failed to clone repository: ${e.message}"
                        error "Failed to clone repository"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    try {
                        docker.build("${DOCKER_IMAGE_NAME}:${IMAGE_TAG}")
                    } catch (Exception e) {
                        echo "Failed to build Docker image: ${e.message}"
                        error "Failed to build Docker image"
                    }
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    try {
                        sh """
                        docker rm -f ${CONTAINER_NAME} || true
                        docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${CONTAINER_PORT} ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}
                        """
                    } catch (Exception e) {
                        echo "Failed to run Docker container: ${e.message}"
                        error "Failed to run Docker container"
                    }
                }
            }
        }

        stage('Verify Container Running') {
            steps {
                script {
                    try {
                        sh """
                        sleep 3
                        STATUS=\$(docker inspect --format='{{.State.Status}}' ${CONTAINER_NAME})
                        echo "Container Status: \$STATUS"
                        
                        if [ "\$STATUS" != "running" ]; then
                            echo "Container is not running!"
                            docker logs ${CONTAINER_NAME}
                            exit 1
                        fi
                        """
                    } catch (Exception e) {
                        echo "Container verification failed: ${e.message}"
                        error "Container verification failed"
                    }
                }
            }
        }
    }

    post {
        always {
            sh "docker rm -f ${CONTAINER_NAME} || true"
        }
    }
}
