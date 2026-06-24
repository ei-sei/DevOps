# 4. Alertmanager

---

## Part 1: What is Alertmanager

What is Alertmanager?
> Alertmanager is a separate component from Prometheus that receives fired alerts and handles deduplicating, grouping, routing, and silencing them before sending notifications.

How does an alert get from Prometheus to Alertmanager?
> Prometheus evaluates alerting rules itself and, when one is firing, sends it to Alertmanager over HTTP. Alertmanager does not evaluate any rules itself.

---

## Part 2: Alerting Rules Recap

Where are alerting rules defined?
> In the Prometheus configuration, as PromQL expressions that, when true for a defined duration, cause an alert to fire.

What does the for clause do in an alerting rule?
> It requires the condition to remain true for a minimum duration before the alert fires, preventing brief spikes from triggering an alert.

What is the difference between pending and firing alert states?
> An alert is **pending** once its condition becomes true but before the `for` duration has elapsed, and becomes **firing** once that duration has passed and it is sent to Alertmanager.

---

## Part 3: Routing

What is a routing tree?
> A routing tree is a hierarchy of rules in Alertmanager's configuration that decides which receiver an alert is sent to, based on its labels.

How does route matching work?
> Each route can match on label values, and child routes can override or narrow the matching of their parent, with the alert ultimately delivered to the first matching leaf route's receiver.

Give an example of routing by severity:
> Alerts labelled `severity="critical"` route to a receiver that pages on-call via PagerDuty, while `severity="warning"` routes to a Slack channel instead.

---

## Part 4: Grouping

What is alert grouping?
> Grouping combines multiple alerts that share specified labels into a single notification, instead of sending one notification per alert.

Why does grouping matter?
> If 50 instances go down at once due to one root cause, grouping sends one notification listing all 50, instead of 50 separate pages.

What do group_wait and group_interval control?
> `group_wait` is how long Alertmanager waits to buffer additional alerts into the first notification of a new group. `group_interval` is how long it waits before sending updates about additional alerts to an existing group.

---

## Part 5: Silencing & Inhibition

What is a silence?
> A silence is a temporary, manually created rule that mutes notifications matching specific labels for a defined time window, typically used during planned maintenance.

What is inhibition?
> Inhibition automatically suppresses certain alerts if another alert is already firing, based on configured rules - for example, suppressing individual instance-down alerts if a whole-cluster-down alert is already firing.

How does inhibition differ from silencing?
> Silencing is manual and time-based. Inhibition is automatic and based on the state of other alerts.

---

## Part 6: Receivers

What is a receiver?
> A receiver is a configured notification target, such as Slack, PagerDuty, email, or a generic webhook, that Alertmanager sends matched alerts to.

Can one alert go to multiple receivers?
> Yes - via `continue: true` on a route, or by matching multiple routes, an alert can be sent to more than one receiver.

---

## Commands to Learn

```bash
# Check Alertmanager config validity
amtool check-config alertmanager.yml
```

```bash
# View currently firing alerts
amtool alert query
```

```bash
# Create a silence from the CLI
amtool silence add alertname="HighErrorRate" --duration=2h --comment="planned maintenance"
```
