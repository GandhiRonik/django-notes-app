pipeline {
    agent any

    environment {
        IMAGE_NAME     = "django_app"
        CONTAINER_NAME = "django_test"
        ENV_FILE       = "/etc/notes-app/.env"
        HEALTH_URL     = "http://localhost:8000/api/health/"
        APP_PORT       = "8000"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "=== Pulling latest code from GitHub ==="
                checkout scm
                echo "=== Checkout complete ==="
            }
        }

        stage('Build') {
            steps {
                echo "=== Building Docker image: ${IMAGE_NAME}:${BUILD_NUMBER} ==="
                sh '''
                    docker build \
                        --no-cache \
                        -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                        -t ${IMAGE_NAME}:latest \
                        .
                '''
                echo "=== Build complete ==="
            }
        }

        stage('Deploy') {
            steps {
                script {
                    env.PREV_IMAGE = sh(
                        script: "docker inspect --format='{{.Config.Image}}' ${CONTAINER_NAME} 2>/dev/null || echo 'none'",
                        returnStdout: true
                    ).trim()
                    echo "Previous image saved: ${env.PREV_IMAGE}"

                    sh '''
                        docker stop ${CONTAINER_NAME} || true
                        docker rm   ${CONTAINER_NAME} || true
                        docker run -d \
                            --name ${CONTAINER_NAME} \
                            --env-file ${ENV_FILE} \
                            -p ${APP_PORT}:${APP_PORT} \
                            --restart unless-stopped \
                            ${IMAGE_NAME}:${BUILD_NUMBER}
                    '''
                    echo "=== Container started ==="
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    def healthy = false
                    for (int attempt = 1; attempt <= 3; attempt++) {
                        echo "Waiting 10s before attempt ${attempt}/3..."
                        sleep(10)
                        def exitCode = sh(
                            script: "curl -sf --max-time 5 ${HEALTH_URL}",
                            returnStatus: true
                        )
                        if (exitCode == 0) {
                            healthy = true
                            echo "Health check PASSED on attempt ${attempt}/3"
                            break
                        }
                        echo "Attempt ${attempt}/3 failed"
                    }
                    if (!healthy) {
                        error("Health check failed after 3 attempts — initiating rollback")
                    }
                }
            }
        }

        stage('Cleanup') {
            steps {
                echo "=== Removing dangling images ==="
                sh 'docker image prune -f || true'
                echo "=== Cleanup complete ==="
            }
        }

    }

    post {
        failure {
            script {
                if (env.PREV_IMAGE && env.PREV_IMAGE != 'none') {
                    echo "=== ROLLING BACK to ${env.PREV_IMAGE} ==="
                    sh '''
                        docker stop ${CONTAINER_NAME} || true
                        docker rm   ${CONTAINER_NAME} || true
                        docker run -d \
                            --name ${CONTAINER_NAME} \
                            --env-file ${ENV_FILE} \
                            -p ${APP_PORT}:${APP_PORT} \
                            --restart unless-stopped \
                            ${PREV_IMAGE}
                    '''
                    echo "=== Rollback complete ==="
                } else {
                    echo "=== No previous image — manual intervention required ==="
                }
            }
        }
        success {
            echo "=== DEPLOYMENT SUCCESSFUL — Build #${BUILD_NUMBER} is live ==="
        }
        always {
            echo "=== Pipeline #${BUILD_NUMBER} finished: ${currentBuild.result} ==="
        }
    }
}
