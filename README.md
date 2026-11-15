# DevOps Demo

A small Python service used to practice a complete delivery path: tests, GitHub Actions, Docker, Kubernetes, Terraform, Prometheus/Grafana, and Argo CD.

## Run locally

```bash
python3 app.py
curl http://localhost:8080/healthz
python3 -m unittest discover -v
```

## Build and run with Docker

```bash
docker build -t devops-demo:latest .
docker run --rm -p 8080:8080 devops-demo:latest
```

## Kubernetes with kind

```bash
kind create cluster --name devops-demo
docker build -t devops-demo:latest .
kind load docker-image devops-demo:latest --name devops-demo
kubectl apply -f k8s/
kubectl port-forward service/devops-demo 8080:80
```

The `ServiceMonitor` requires the Prometheus Operator or the kube-prometheus-stack. Without that operator, apply `deployment.yaml` and `service.yaml` only.

## Monitoring

Run the local monitoring stack with `docker compose -f docker-compose.monitoring.yml up --build`. The app is available at `http://localhost:8080`, Prometheus at `http://localhost:9090`, and Grafana at `http://localhost:3000`.

## Terraform on AWS

The Terraform example creates a small EC2 instance, opens HTTP/SSH, installs Docker, and starts the published image. Create `terraform/terraform.tfvars` locally with an existing key pair and a restricted SSH CIDR, then run:

```bash
cd terraform
terraform init
terraform plan -var='key_name=YOUR_EC2_KEY_NAME'
terraform apply -var='key_name=YOUR_EC2_KEY_NAME'
```

Run `terraform destroy` when finished. Do not commit credentials, state files, or a real key name.

## Argo CD GitOps

1. Replace the repository URL in `argocd/application.yaml`.
2. Install Argo CD in the cluster.
3. Apply the application manifest: `kubectl apply -f argocd/application.yaml`.
4. Change and push a manifest in `k8s/`; Argo CD will reconcile the cluster.

The CI workflow runs unit tests and builds the image on pushes to `main` and pull requests. Publishing to GHCR can be added after the repository name is known, using `GITHUB_TOKEN` and an image tag based on the commit SHA.