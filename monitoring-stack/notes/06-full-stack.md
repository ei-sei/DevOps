# 6. Full Stack: Docker Compose Walkthrough

---

## Objective

Bring up Prometheus, Grafana, Alertmanager, node_exporter, and Loki together with a single `docker-compose.yml`, confirm metrics are flowing end to end, and fire one alert through Alertmanager.

## Architecture

> node_exporter exposes host metrics -> Prometheus scrapes node_exporter and evaluates alerting rules -> firing alerts are sent to Alertmanager -> Grafana queries Prometheus for dashboards and Loki for logs.

## docker-compose.yml

```yaml
version: "3.8"

services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alert.rules.yml:/etc/prometheus/alert.rules.yml
    ports:
      - "9090:9090"

  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"

  alertmanager:
    image: prom/alertmanager:latest
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
    ports:
      - "9093:9093"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"

  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"

  promtail:
    image: grafana/promtail:latest
    volumes:
      - /var/log:/var/log
      - ./promtail.yml:/etc/promtail/promtail.yml
```

## prometheus.yml

```yaml
global:
  scrape_interval: 15s

rule_files:
  - "alert.rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

scrape_configs:
  - job_name: "node"
    static_configs:
      - targets: ["node-exporter:9100"]
```

## alert.rules.yml

```yaml
groups:
  - name: example
    rules:
      - alert: HighCPULoad
        expr: 1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) > 0.8
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "CPU load is above 80% for 2 minutes"
```

## Steps

1. Run `docker compose up -d` and confirm all five containers are healthy with `docker compose ps`.
2. Visit `http://localhost:9090/targets` and confirm the `node` job shows as `UP`.
3. In Grafana (`http://localhost:3000`), add Prometheus (`http://prometheus:9090`) and Loki (`http://loki:3100`) as data sources.
4. Build a dashboard panel querying `node_cpu_seconds_total` and confirm it renders.
5. Generate CPU load on the host (e.g. `yes > /dev/null &`) until `HighCPULoad` fires, then confirm it appears under `http://localhost:9093` in Alertmanager.

---

## Part 1: Why Wire It All Together

What does this lab prove that reading the individual tool notes does not?
> That the pieces actually integrate - Prometheus reads node_exporter, Alertmanager receives what Prometheus fires, and Grafana can visualise both Prometheus and Loki at once. Each tool's notes cover it in isolation; this confirms the data path works end to end.

Why use Docker Compose instead of installing each tool manually?
> Compose lets the whole stack be defined, started, and torn down as one unit, and mirrors how this kind of stack is often run in development or small production setups.

What is the first thing to check if Grafana shows no data?
> Whether Prometheus's `/targets` page shows the target as `UP` - if the target itself isn't being scraped successfully, nothing further down the chain will have data either.

---

## Commands to Learn

```bash
# Start the full stack
docker compose up -d
```

```bash
# Check container health
docker compose ps
```

```bash
# Tail logs for a specific service
docker compose logs -f prometheus
```

```bash
# Tear down the stack
docker compose down
```
