# 2. Prometheus

---

## Part 1: What is Prometheus

What is Prometheus?
> Prometheus is an open-source monitoring system that collects and stores metrics as time series data, with a built-in query language and alerting engine.

What are the core components of Prometheus?
> The Prometheus server (scraping and storage), exporters (expose metrics from systems that do not natively support Prometheus), Alertmanager (handles alert routing), and client libraries (instrument application code directly).

Is Prometheus push or pull based?
> Pull based - Prometheus scrapes an HTTP endpoint on each target at a configured interval, rather than targets pushing data to it.

---

## Part 2: The Pull Model & Scrape Config

What does a target need to expose for Prometheus to scrape it?
> An HTTP endpoint, conventionally `/metrics`, returning metrics in Prometheus's plain text exposition format.

What is a scrape config?
> A scrape config is a block in `prometheus.yml` that defines which targets to scrape, how often, and under what job name.

What is a scrape interval?
> The frequency at which Prometheus pulls metrics from a target, commonly every 15 or 30 seconds.

What is a job in Prometheus?
> A job is a logical group of targets performing the same role, such as all instances of a particular service, labelled with a job name for querying.

---

## Part 3: Service Discovery

What problem does service discovery solve?
> Manually listing every target in a static config does not scale in dynamic environments where instances are constantly created and destroyed, such as Kubernetes or Auto Scaling Groups.

What service discovery mechanisms does Prometheus support?
> Kubernetes SD, EC2 SD, Consul SD, file-based SD, and several others, which automatically discover and update the list of scrape targets.

How does Kubernetes service discovery work in Prometheus?
> Prometheus queries the Kubernetes API for pods, services, and endpoints matching configured selectors, and automatically adds or removes them as scrape targets as the cluster changes.

---

## Part 4: Exporters

What is an exporter?
> An exporter is a small process that converts metrics from a system that does not natively speak Prometheus's format into a `/metrics` endpoint Prometheus can scrape.

What does node_exporter expose?
> Host-level metrics such as CPU, memory, disk, and network usage for a Linux or Windows machine.

What does cAdvisor or kube-state-metrics expose?
> cAdvisor exposes per-container resource usage, while kube-state-metrics exposes the state of Kubernetes objects themselves, such as deployment replica counts and pod status.

When would you instrument your own application instead of using an exporter?
> When you want custom business metrics, such as orders processed or queue depth, by adding a Prometheus client library directly to your application code.

---

## Part 5: Data Model & Metric Types

What is a time series in Prometheus?
> A time series is a stream of timestamped values identified by a metric name and a unique set of key-value labels.

What is a label?
> A label is a key-value pair attached to a metric that lets you filter and group time series, such as `method="GET"` or `status="500"`.

What is cardinality and why does it matter?
> Cardinality is the number of unique label combinations for a metric. High cardinality, such as using a label for every unique user ID, can overwhelm Prometheus's storage and query performance.

What are the four core metric types?
> **Counter**, **Gauge**, **Histogram**, and **Summary**.

What is a Counter?
> A Counter is a value that only increases, such as total requests served, used to calculate rates over time.

What is a Gauge?
> A Gauge is a value that can go up or down, such as current memory usage or number of active connections.

What is a Histogram?
> A Histogram samples observations, such as request durations, into configurable buckets, allowing you to calculate quantiles and averages after the fact.

What is a Summary and how does it differ from a Histogram?
> A Summary also samples observations but calculates quantiles on the client side before exposing them, which makes aggregation across instances inaccurate, whereas Histogram buckets can be aggregated correctly on the server side.

---

## Part 6: PromQL Basics

What is an instant vector?
> An instant vector is a set of time series, each with a single value, at a single point in time.

What is a range vector?
> A range vector is a set of time series with a range of data points over a time window, written as `metric_name[5m]`.

How do you filter a metric by label?
> Using curly braces, e.g. `http_requests_total{status="500"}` returns only the time series matching that label.

What does the rate() function do?
> `rate()` calculates the per-second average rate of increase of a Counter over a given time window, automatically handling counter resets.

Why use rate() instead of just subtracting two raw values?
> Counters reset to zero when a process restarts, so a naive subtraction can produce a negative or misleading number. `rate()` detects and corrects for resets.

---

## Part 7: PromQL Aggregation

What are aggregation operators in PromQL?
> Functions like `sum()`, `avg()`, `max()`, `min()`, and `count()` that combine multiple time series into fewer results.

What does the by() clause do?
> `by()` keeps specified labels when aggregating, so you can group results, e.g. `sum(rate(http_requests_total[5m])) by (status)` gives request rate per status code.

Give an example of calculating an error rate with PromQL:
> `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))` gives the proportion of requests that returned a 5xx error.

---

## Part 8: Recording Rules

What is a recording rule?
> A recording rule precomputes a frequently used or expensive PromQL expression on a schedule and saves the result as a new time series, so dashboards and alerts can query it cheaply.

When should you use a recording rule?
> When a query is computationally expensive, used in multiple dashboards, or evaluated repeatedly by alerting rules.

---

## Part 9: Storage

How does Prometheus store data?
> In a custom time series database (TSDB) on local disk, organised into immutable two-hour blocks plus a write-ahead log for crash recovery.

What is the default retention period?
> 15 days, though it is configurable.

Why is Prometheus not meant for long-term storage by default?
> Local disk storage does not scale well for years of data or high availability, which is why remote write to long-term storage systems like Thanos, Cortex, or Mimir is used for that purpose.

---

## Commands to Learn

```bash
# Check Prometheus config validity
promtool check config prometheus.yml
```

```bash
# Query Prometheus via its HTTP API
curl 'http://localhost:9090/api/v1/query?query=up'
```

```bash
# Run node_exporter
./node_exporter --web.listen-address=:9100
```

```bash
# Reload Prometheus config without restarting
curl -X POST http://localhost:9090/-/reload
```
