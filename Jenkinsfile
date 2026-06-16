pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'jerry1808/mj-gitops-app'
        MANIFESTS_REPO = 'https://github.com/0xJeevs/mj-gitops-manifests.git'
        DOCKER_CREDENTIALS = credentials('dockerhub')
        GIT_CREDENTIALS = credentials('git-credentials')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    echo "Building image with tag: ${env.COMMIT_HASH}"
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    echo "Running tests..."
                    // Add your test commands here
                    // For now, we'll just verify the app structure
                    sh 'ls -la'
                    sh 'cat requirements.txt'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    sh "docker build -t ${DOCKER_IMAGE}:${env.COMMIT_HASH} ."
                    sh "docker tag ${DOCKER_IMAGE}:${env.COMMIT_HASH} ${DOCKER_IMAGE}:latest"
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing to Docker Hub..."
                    sh """
                        echo ${DOCKER_CREDENTIALS_PSW} | docker login -u ${DOCKER_CREDENTIALS_USR} --password-stdin
                        docker push ${DOCKER_IMAGE}:${env.COMMIT_HASH}
                        docker push ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }
        
        stage('Update GitOps Manifests') {
            steps {
                script {
                    echo "Updating Kubernetes manifests..."
                    sh """
                        git config --global user.email "jenkins@mj-gitops.com"
                        git config --global user.name "Jenkins CI"
                        
                        # Clone manifests repo
                        git clone ${MANIFESTS_REPO} manifests-temp
                        cd manifests-temp
                        
                        # Update the image tag in deployment.yaml
                        sed -i "s|image: jerry1808/mj-gitops-app:.*|image: ${DOCKER_IMAGE}:${env.COMMIT_HASH}|g" deployment.yaml
                        
                        # Commit and push
                        git add deployment.yaml
                        git commit -m "Update image tag to ${env.COMMIT_HASH} [skip ci]"
                        git push https://${GIT_CREDENTIALS_USR}:${GIT_CREDENTIALS_PSW}@github.com/0xJeevs/mj-gitops-manifests.git main
                    """
                }
            }
        }
    }
    
    post {
        always {
            echo "Pipeline completed!"
            cleanWs()
        }
        success {
            echo "Pipeline succeeded! New image deployed: ${DOCKER_IMAGE}:${env.COMMIT_HASH}"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}
