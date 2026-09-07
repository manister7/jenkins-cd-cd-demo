pipeline {
    agent { label 'built-in'}

    environment {
        IMAGE_NAME = "manister7/jenkins-cd-cd-demo"
        VERSION = "v${env.BUILD_NUMBER}"
        }
    
    stages{
        stage('Checkout') {
            steps {
                git (
                    url: 'https://github.com/manister7/jenkins-cd-cd-demo.git', 
                    branch: 'main',
                    credentialsId: 'e0a5f626-68bf-4696-bea8-2d9e833f6753'  
                )
            }
        }

        stage('Install and Test') {
            steps {
                sh '''
                    #!/bin/bash
                    python3 -m venv venv
                    venv/bin/pip install -r backend/requirements.txt
                    PYTHONPATH=. venv/bin/pytest backend/tests/test_app.py --junitxml=results.xml
                '''
            }
            post {
                always {
                    junit 'results.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$VERSION .'
                sh 'docker tag $IMAGE_NAME:$VERSION $IMAGE_NAME:latest'
            }
        }

        stage('Push to dockerhub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $IMAGE_NAME:$VERSION'
                    sh 'docker push $IMAGE_NAME:latest'
                }
            }
        }

        stage("Verify Image") {
        steps {
            sh 'docker run --rm -p 5000:5000 $IMAGE_NAME:$VERSION & sleep 300 && curl -s http://localhost:5000/dog'
        }
        }
    }
}