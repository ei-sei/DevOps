# 3. Grafana

---

## Part 1: What is Grafana

What is Grafana?
> Grafana is an open-source visualisation and dashboarding tool that queries data sources like Prometheus and renders the results as graphs, tables, and other panels.

Does Grafana store metrics itself?
> No - Grafana is a visualisation layer only. It queries external data sources for data and has no time series storage of its own.

---

## Part 2: Data Sources

What is a data source in Grafana?
> A data source is a configured connection to a backend system, such as Prometheus, Loki, or a SQL database, that Grafana queries to populate panels.

Can a single dashboard use multiple data sources?
> Yes - different panels on the same dashboard can each query a different data source.

---

## Part 3: Dashboards & Panels

What is a panel?
> A panel is a single visualisation on a dashboard, such as a time series graph, a table, or a stat box, each backed by one or more queries.

What is a dashboard?
> A dashboard is a collection of panels arranged on a page, typically focused on one service or concern.

What panel types are commonly used?
> Time series for trends over time, Stat for a single current value, Gauge for a value against thresholds, and Table for raw query results.

---

## Part 4: Variables & Templating

What is a dashboard variable?
> A variable is a placeholder in a dashboard, such as `$environment` or `$instance`, that lets viewers switch what the dashboard displays without editing the underlying queries.

Give an example of using a variable:
> A query variable populated from `label_values(up, instance)` lets a dropdown list every instance, and panels use `{instance="$instance"}` to filter to the selected one.

Why are variables useful for reusable dashboards?
> They let one dashboard definition serve many services or environments, instead of duplicating the dashboard for each one.

---

## Part 5: Grafana Alerting vs Alertmanager

Can Grafana fire alerts on its own?
> Yes - Grafana has its own built-in alerting engine that can evaluate queries and fire alerts independently of Prometheus's Alertmanager.

When would you use Grafana alerting instead of Prometheus alerting rules?
> When your data source is not Prometheus, or when you want a single place to manage alerts across multiple different data sources.

When would you prefer Prometheus alerting rules and Alertmanager instead?
> When you are already invested in the Prometheus ecosystem and want alerting rules to live alongside recording rules, version-controlled as part of your Prometheus configuration.

---

## Part 6: Provisioning as Code

What does it mean to provision Grafana as code?
> Defining data sources and dashboards as JSON or YAML files checked into version control, rather than clicking through the UI, so they can be deployed consistently and reviewed like any other code change.

How does Grafana load provisioned dashboards on startup?
> By reading YAML provisioning files that point to a directory of dashboard JSON files, which Grafana loads automatically when the container or service starts.

What is a benefit of dashboards as code?
> Changes are reviewable in pull requests, reproducible across environments, and not lost if someone accidentally edits a dashboard in the UI.

---

## Commands to Learn

```bash
# Run Grafana locally via Docker
docker run -d -p 3000:3000 --name=grafana grafana/grafana
```

```bash
# Add a data source via the HTTP API
curl -X POST http://admin:admin@localhost:3000/api/datasources \
  -H "Content-Type: application/json" \
  -d '{"name":"Prometheus","type":"prometheus","url":"http://localhost:9090","access":"proxy"}'
```

```bash
# Export a dashboard as JSON via the API
curl http://admin:admin@localhost:3000/api/dashboards/uid/<uid>
```
