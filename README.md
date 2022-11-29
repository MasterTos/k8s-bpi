# k8s-bpi

## install metrics-server
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

## install ingress
```bash
helm upgrade --install ingress-nginx ingress-nginx \
--repo https://kubernetes.github.io/ingress-nginx \
--namespace ingress-nginx --create-namespace \
--set controller.metrics.enabled=true \
--set-string controller.podAnnotations."prometheus\.io/scrape"="true" \
--set-string controller.podAnnotations."prometheus\.io/port"="10254"
```

## Postgres
```bash
kubectl exec -it [pod-name] --  psql -h localhost -U admin --password -p 5432 postgresdb
```


## Grafana

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

```bash
helm install [RELEASE_NAME] prometheus-community/kube-prometheus-stack
```


```bash
https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/grafana/dashboards/nginx.json
```


```bash
helm upgrade --install monitor --namespace monitor --create-namespace -f prom-custom-values.yaml prometheus-community/kube-prometheus-stack
```

```bash
helm upgrade prometheus -f prom-custom-values.yaml prometheus-community/kube-prometheus-stack
```


```bash
kubectl get secrets -n monitor monitor-grafana -o jsonpath='{.data.admin-password}' | base64 -d
```

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-release bitnami/grafana-loki
```