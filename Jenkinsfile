pipeline {
    agent any

    environment {
        IMAGE_NAME     = "django_app"
        CONTAINER_NAME = "django_test"
        ENV_FILE       = "/etc/notes-app/.env"
        HEALTH_URL     = "http://localhost:8000/api/health/"
        APP_PORT       = "8000"
    }

    // ── BITBUCKET WEBHOOK TRIGGER ──────────────────────────────────────────────
    triggers {
        GenericTrigger(
            genericVariables: [
                [key: 'PR_STATE',      value: '$.pullrequest.state'],
                [key: 'TARGET_BRANCH', value: '$.pullrequest.destination.branch.name']
            ],
            token: 'bitbucket-crm-deploy',
            causeString: 'Triggered by Bitbucket PR merge',
            printContributedVariables: false,
            printPostContent: false,
            regexpFilterText:       '$PR_STATE#$TARGET_BRANCH',
            regexpFilterExpression: '^MERGED#production$'
        )
    }

    stages {
        stage('Checkout') {
            steps {
                echo "=== Pulling latest code from GitHub/Bitbucket ==="
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
                    // Save the currently running image ID for rollback purposes
                    env.PREV_IMAGE = sh(
                        script: "docker inspect --format='{{.Config.Image}}' ${CONTAINER_NAME} 2>/dev/null || echo 'none'",
                        returnStdout: true
                    ).trim()
                    echo "Previous image saved: ${env.PREV_IMAGE}"

                    // Stop old container and spin up the new one
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
            // Rollback to the previous Docker image if the deployment or health check fails
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
            echo "❌ Deployment FAILED. Check Jenkins console. Rollback initiated."
        }
        
        success {
            echo "✅ Deployment SUCCEEDED. Deployed commit: ${env.GIT_COMMIT ?: 'unknown'}"
            
            // ── EMAIL NOTIFICATION (RESTRICTED TO SUCCESS) ─────────────────────────
            script {
                emailext(
                    to: 'ronikgandhi54@gmail.com',
                    subject: "✅ [django_app] Deployment Successful — Build #${env.BUILD_NUMBER}",
                    body: """
<html>
<body style="font-family: Arial, sans-serif; color: #333;">
    <h2 style="color: #2e7d32;">✅ Deployment Successful</h2>
    <table cellpadding="8" cellspacing="0" border="1" style="border-collapse: collapse;">
        <tr><td><b>Project</b></td><td>Django Notes App</td></tr>
        <tr><td><b>Environment</b></td><td>Production</td></tr>
        <tr><td><b>Build #</b></td><td>${env.BUILD_NUMBER}</td></tr>
        <tr><td><b>Commit</b></td><td>${env.GIT_COMMIT ?: 'unknown'}</td></tr>
        <tr><td><b>Triggered by</b></td><td>${env.BUILD_CAUSE ?: 'Bitbucket PR merge'}</td></tr>
        <tr><td><b>Duration</b></td><td>${currentBuild.durationString}</td></tr>
        <tr><td><b>Console Log</b></td><td><a href="${env.BUILD_URL}console">${env.BUILD_URL}console</a></td></tr>
    </table>
    <p style="margin-top: 16px; color: #555;">All stages completed successfully including the container health check.</p>
</body>
</html>
                    """,
                    mimeType: 'text/html'
                )
            }
        }
        
        always {
            echo "=== Pipeline #${BUILD_NUMBER} finished: ${currentBuild.result} ==="
            // Workspace cleanup runs regardless of success or failure
            cleanWs(cleanWhenAborted: true, cleanWhenFailure: false, cleanWhenSuccess: true)
        }
    }
}
