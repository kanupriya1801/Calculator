pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "kanupriya18/calculator-app"
        DOCKER_CREDENTIALS_ID = "dockerhub-creds"
        HELM_RELEASE_NAME = "calculator-release"
        HELM_CHART_NAME = "to-do-chart"
        KUBE_CONTEXT = "minikube"
        JIRA_SITE = "your-jira-site"
        JIRA_CREDENTIALS_ID = "jira-creds"
    }

    triggers {
        githubPush() // Triggered when PR is merged to main
    }

    options {
        skipDefaultCheckout()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('', DOCKER_CREDENTIALS_ID) {
                        dockerImage.push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes with Helm') {
            steps {
                script {
                    sh """
                        helm upgrade --install ${HELM_RELEASE_NAME} ./${HELM_CHART_NAME} \
                        --set image.repository=${DOCKER_IMAGE} \
                        --set image.tag=${env.BUILD_NUMBER} \
                        --kube-context ${KUBE_CONTEXT}
                    """
                }
            }
        }

        stage('Update Jira') {
            steps {
                jiraSendBuildInfo site: JIRA_SITE, buildNumber: env.BUILD_NUMBER
                jiraSendDeploymentInfo site: JIRA_SITE, environmentId: 'production', environmentName: 'Production', deploymentState: 'successful'
            }
        }
    }
}
