# 1. Foundations

---

## Part 1: Why Observability Matters

What is observability?
> Observability is the ability to understand what is happening inside a system from the outside, using the data it produces, without needing to ship new code to investigate a problem.

Why isn't "is the server up" enough?
> A server can be up and still fail silently - slow responses, partial outages, or a single broken dependency can degrade the user experience without ever taking the whole service offline. Observability surfaces these partial failures, not just total ones.

What is the difference between monitoring and observability?
> Monitoring tells you when something you already expected to fail has failed, based on predefined checks. Observability gives you the data to investigate problems you did not anticipate, by letting you ask new questions of the system after the fact.

---

## Part 2: The Three Pillars

What are the three pillars of observability?
> Metrics, logs, and traces.

What is a metric?
> A metric is a numeric measurement recorded over time, such as request count or CPU usage. Metrics are cheap to store and ideal for trends, dashboards, and alerting.

What is a log?
> A log is a timestamped, discrete record of an event, such as an error message or a request being handled. Logs are detailed but expensive to store and search at scale.

What is a trace?
> A trace follows a single request as it moves through multiple services, recording how long each step took. Traces are essential for diagnosing latency in distributed systems.

When would you reach for each pillar?
> Metrics to notice something is wrong, logs to find the specific event that caused it, and traces to understand where time was lost across services.

---

## Part 3: Pull vs Push Monitoring

What is pull-based monitoring?
> In pull-based monitoring, the monitoring system reaches out and scrapes metrics from each target on a schedule. Prometheus works this way.

What is push-based monitoring?
> In push-based monitoring, each service actively sends its metrics to a central collector. Many APM tools and StatsD-based systems work this way.

What is an advantage of pull-based monitoring?
> The monitoring system controls the scrape schedule and can detect a target going down simply by failing to scrape it, which doubles as a basic health check.

What is an advantage of push-based monitoring?
> It works well for short-lived jobs that may not exist long enough to be scraped, such as batch jobs or serverless functions.

---

## Part 4: RED Method

What does RED stand for?
> Rate, Errors, and Duration.

What does each part of RED measure?
> Rate is the number of requests per second, Errors is the number or percentage of failed requests, and Duration is how long requests take to complete.

What is RED designed for?
> Monitoring request-driven services, such as APIs and web applications.

---

## Part 5: USE Method

What does USE stand for?
> Utilisation, Saturation, and Errors.

What does each part of USE measure?
> Utilisation is how busy a resource is, Saturation is how much work is queued waiting for that resource, and Errors is the count of error events on that resource.

What is USE designed for?
> Monitoring infrastructure resources, such as CPU, memory, disk, and network.

How do RED and USE complement each other?
> RED tells you something is wrong with a service, USE tells you why, by pointing at the underlying resource that is overloaded.

---

## Part 6: SLIs, SLOs, and SLAs

What is an SLI?
> A **Service Level Indicator** is a specific measured value, such as "99.95% of requests returned successfully in the last 30 days."

What is an SLO?
> A **Service Level Objective** is the target you set for an SLI, such as "99.9% of requests should succeed."

What is an SLA?
> A **Service Level Agreement** is a contractual promise to a customer, usually with financial or contractual consequences if the SLO it is based on is breached.

What is an error budget?
> An **error budget** is the allowed amount of failure within an SLO - if your SLO is 99.9% uptime, your error budget is the remaining 0.1%, which you can spend on deployments, experiments, or accept as ongoing risk.

---

## Part 7: Alerting Philosophy

What makes a good alert?
> A good alert is actionable - it tells you something a human needs to act on right now, not just that a number crossed a threshold.

What is alert fatigue?
> Alert fatigue happens when a system fires too many low-value or noisy alerts, causing on-call engineers to start ignoring or muting them, including the ones that actually matter.

What should you alert on instead of raw metrics?
> Symptoms that affect users, such as error rate or latency breaching an SLO, rather than every internal cause - alert on the SLO burn rate, then use dashboards and logs to investigate the cause.
