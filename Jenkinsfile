pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "kanupriya18/calculator-app"
        DOCKER_CREDENTIALS_ID = "dockerhub-creds"
        HELM_RELEASE_NAME = "calculator-release"
        HELM_CHART_NAME = "to-do-chart"
        //KUBE_CONTEXT = "minikube"
        OPENSHIFT_HELM_RELEASE_NAME = "calculator-green"
        OPENSHIFT_HELM_CHART_NAME = "calculator-chart-openshift"
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
                        --kubeconfig /var/lib/jenkins/.kube/config
                    """
                }
            }
        }
        stage('Deploy to Kubernetes (Blue)') {
            steps {
                script {
                    sh """
                       helm upgrade --install calculator-release ./to-do-chart \
                       --set image.repository=${DOCKER_IMAGE} \
                       --set image.tag=${env.BUILD_NUMBER} \
                       --kubeconfig /var/lib/jenkins/.kube/config
                    """
                   }
              }
        } 
        stage('Deploy to OpenShift (Green)') {
            steps {
                script {
                    sh """
                       helm upgrade --install ${OPENSHIFT_HELM_RELEASE_NAME} ./${OPENSHIFT_HELM_CHART_NAME} \
                       --set image.repository=${DOCKER_IMAGE} \
                       --set image.tag=${env.BUILD_NUMBER} \
                       --kube-context openshift-sandbox \
                       --namespace green --create-namespace
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
