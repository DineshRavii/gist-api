pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/DineshRavii/gist-api.git'
            }
        }

        stage('Test') {
            agent {
                docker {
                    image 'python:3.12-slim'
                    reuseNode true
                }
            }
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip3 install -r requirements.txt
                    pytest test_app.py -v
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t gist-api:latest .'
            }
        }

        stage('Docker deploy') {
            steps{
                sh '''
                    docker stop gist-api || true
                    docker rm gist-api || true
                    docker run -d -p 8080:8080 --name gist-api gist-api:latest
                '''
            }
        }

        // stage('deploy in k8s') {
        //     steps {
        //             sh '''
        //                 kubectl set image deployment/gist-api \
        //                 gist-api=ghcr.io/dineshravii/gist-api:latest
        //                 kubectl rollout status deployment/gist-api
        //             '''
        //          }
        // }
    }
}