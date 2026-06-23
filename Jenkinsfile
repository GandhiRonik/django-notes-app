pipeline {
    agent any

    environment {
        IMAGE_NAME     = "django_app"
        CONTAINER_NAME = "django_test"
        HEALTH_URL     = "http://localhost:8000/api/health/"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/GandhiRonik/django-notes-app.git'
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
                sh 'docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest'
            }
        }

        stage('Test') {
            steps {
                sh '''
                    docker run --rm \
                      --env-file /etc/notes-app/.env \
                      ${IMAGE_NAME}:${BUILD_NUMBER} \
                      python manage.py test --verbosity=2
                '''
            }
        }

        stage('Deploy') {
            steps {
                script {
                    env.PREV_IMAGE = sh(
                        script: "docker inspect --format='{{.Config.Image}}' ${CONTAINER_NAME} 2>/dev/null || echo 'none'",
                        returnStdout: true
                    ).trim()

                    sh '''
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                        docker run -d \
                          --name ${CONTAINER_NAME} \
                          --env-file /etc/notes-app/.env \
                          -p 8000:8000 \
                          --restart unless-stopped \
                          ${IMAGE_NAME}:${BUILD_NUMBER}
                    '''
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    def healthy = false
                    for (int i = 0; i < 3; i++) {
                        sleep(10)
                        def status = sh(
                            script: "curl -sf --max-time 5 ${HEALTH_URL}",
                            returnStatus: true
                        )
                        if (status == 0) {
                            healthy = true
                            echo "Health check passed on attempt ${i + 1}"
                            break
                        }
                        echo "Attempt ${i + 1}/3 failed — waiting 10s"
                    }
                    if (!healthy) {
                        error("Health check failed after 3 attempts — triggering rollback")
                    }
                }
            }
        }

    }

    post {
        failure {
            script {
                if (env.PREV_IMAGE && env.PREV_IMAGE != 'none') {
                    echo "Rolling back to ${env.PREV_IMAGE}"
                    sh '''
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                        docker run -d \
                          --name ${CONTAINER_NAME} \
                          --env-file /etc/notes-app/.env \
                          -p 8000:8000 \
                          --restart unless-stopped \
                          ${PREV_IMAGE}
                    '''
                } else {
                    echo "No previous image — skipping rollback"
                }
            }
        }
        always {
            sh 'docker image prune -f || true'
        }
    }
}
