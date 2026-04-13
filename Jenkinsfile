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
    }
}