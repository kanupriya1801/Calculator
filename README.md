# OpenShift Clients

The OpenShift client `oc` simplifies working with Kubernetes and OpenShift
clusters, offering a number of advantages over `kubectl` such as easy login,
kube config file management, and access to developer tools. The `kubectl`
binary is included alongside for when strict Kubernetes compliance is necessary.

To learn more about OpenShift, visit [docs.openshift.com](https://docs.openshift.com)
and select the version of OpenShift you are using.

## Installing the tools

After extracting this archive, move the `oc` and `kubectl` binaries
to a location on your PATH such as `/usr/local/bin`. Then run:

    oc login [API_URL]

to start a session against an OpenShift cluster. After login, run `oc` and
`oc help` to learn more about how to get started with OpenShift.

## License

OpenShift is licensed under the Apache Public License 2.0. The source code for this
program is [located on github](https://github.com/openshift/oc).

# DevOps Project Showcase: Calculator App

This README outlines the complete setup and demo plan for showcasing the Calculator App DevOps project on a Pluralsight EC2 sandbox.

## 🔧 Technologies Used
- **GitHub**: Source code and version control
- **Jenkins**: CI/CD pipeline automation
- **Docker**: Containerization of the application
- **Minikube**: Local Kubernetes cluster for blue environment
- **OpenShift**: Cloud-native Kubernetes platform for green environment
- **Helm**: Package manager for Kubernetes deployments
- **Prometheus & Grafana**: Monitoring and visualization stack
- **New Relic**: Infrastructure and application monitoring

## 📁 Project Structure
- `Dockerfile`: Container build instructions
- `Jenkinsfile`: CI/CD pipeline definition
- `to-do-chart/`: Helm chart for Kubernetes (blue)
- `chart-openshift/`: Helm chart for OpenShift (green)

## 🚀 Setup Instructions

### 1. Start Minikube
```bash
minikube start
```

### 2. Build Docker Image in Minikube
```bash
eval $(minikube -p minikube docker-env)
docker build -t calculator-app:latest .
```

### 3. Deploy to Kubernetes (Blue)
```bash
helm upgrade --install calculator ./to-do-chart   --set image.repository=calculator-app   --set image.tag=latest   --namespace dev --create-namespace
```

### 4. Expose App via NodePort
```bash
kubectl expose deployment calculator   --type=NodePort   --port=8080   --target-port=8080   --name=calculator-service   --namespace=dev
```

### 5. Get Access URL
```bash
minikube service calculator-service -n dev --url
```

### 6. Start Jenkins
```bash
sudo systemctl start jenkins
```
Access Jenkins at:
```
http://<sandbox-ip>:8080
```

### 7. Deploy to OpenShift (Green)
```bash
oc login --token=<your-token> --server=https://api.rm1.0a51.p1.openshiftapps.com:6443
kubectl config rename-context "<original-context>" openshift-sandbox
helm upgrade --install calculator-green ./chart-openshift   --set image.repository=kanupriya18/calculator-app   --set image.tag=latest   --kube-context openshift-sandbox   --namespace green --create-namespace
```

### 8. Monitoring Stack (Optional)
#### Prometheus
```bash
helm install prometheus prometheus-community/prometheus   --namespace monitoring --create-namespace   --set server.service.type=NodePort
```
#### Grafana
```bash
helm install grafana grafana/grafana   --namespace monitoring   --set service.type=NodePort   --set adminPassword='admin'
```
#### Access Grafana
```bash
minikube service grafana -n monitoring --url
```

## 🎯 Demo Flow
1. Show GitHub repo with Jenkinsfile, Dockerfile, Helm charts
2. Run Jenkins pipeline → build Docker image → deploy to Minikube and OpenShift
3. Access app via Minikube and OpenShift route
4. Show Grafana dashboards (if configured)
5. Explain blue/green strategy
6. Highlight New Relic integration (optional)
