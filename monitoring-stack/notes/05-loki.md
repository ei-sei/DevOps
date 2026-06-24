# 5. Loki

---

## Part 1: What is Loki

What is Loki?
> Loki is a log aggregation system built by Grafana Labs, designed to be cost-efficient by indexing only metadata labels rather than the full text of every log line.

How does Loki's approach differ from tools like Elasticsearch?
> Elasticsearch indexes the full content of every log line for fast full-text search, which is powerful but expensive to store and run at scale. Loki only indexes labels, then compresses and stores raw log content cheaply, trading some query flexibility for much lower cost.

Why is Loki often paired with Prometheus and Grafana?
> It deliberately mirrors Prometheus's label-based model, so the same labels you use to query metrics can be used to query related logs, and Grafana can display both side by side.

---

## Part 2: Labels & Cardinality

What is a label in Loki?
> A label is a key-value pair attached to a log stream, such as `app="checkout"` or `environment="prod"`, used to select which streams to search.

Why is high cardinality a bigger problem in Loki than it sounds?
> Each unique combination of label values creates a separate stream, and an explosion of streams, such as labelling by request ID, can overwhelm Loki's index and badly degrade performance.

---

## Part 3: LogQL

What is LogQL?
> LogQL is Loki's query language, modelled closely on PromQL, used to select log streams by label and then filter or parse their content.

What does a basic LogQL query look like?
> `{app="checkout"} |= "error"` selects the checkout app's log stream and filters lines containing the text "error".

Can LogQL calculate metrics from logs?
> Yes - functions like `rate()` and `count_over_time()` can turn log line counts into time series, e.g. counting errors per second, similar to PromQL.

---

## Part 4: Log Collection Agents

What is Promtail?
> Promtail is Loki's original log collection agent, which tails log files on a host, attaches labels, and pushes log lines to Loki.

What is replacing Promtail in newer Loki deployments?
> Grafana Alloy, Grafana Labs's unified collector, is the recommended replacement, though Promtail remains widely used and supported.

How does a log collection agent decide which labels to attach?
> Through configured scrape and relabeling rules, often similar in syntax to Prometheus's relabeling, commonly deriving labels from file paths, Kubernetes pod metadata, or static config.

---

## Part 5: Loki + Grafana Integration

How do you query Loki from Grafana?
> By adding Loki as a data source, then using its Explore view or building dashboard panels with LogQL queries, the same way you would with Prometheus and PromQL.

What is a common workflow linking metrics and logs?
> Spotting an anomaly on a Prometheus-backed dashboard, then jumping to Loki logs filtered by the same labels and time range to find the specific error that caused it.

---

## Commands to Learn

```bash
# Run Loki locally via Docker
docker run -d -p 3100:3100 grafana/loki:latest
```

```bash
# Run Promtail with a config file
promtail -config.file=promtail-config.yaml
```

```bash
# Query Loki directly via its HTTP API
curl -G -s "http://localhost:3100/loki/api/v1/query_range" \
  --data-urlencode 'query={app="checkout"}'
```
