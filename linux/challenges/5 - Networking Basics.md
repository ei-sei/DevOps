### Real-World Context

Every DevOps role involves networking. You'll troubleshoot connectivity issues, verify services are listening, and download files.

### Windows ↔ Linux Bridge

| Windows      | Linux              | Notes            |
| ------------ | ------------------ | ---------------- |
| `ipconfig`   | `ip addr`          | View IP config   |
| `ping`       | `ping`             | Test connectivity|
| `tracert`    | `traceroute`       | Trace route      |
| `netstat -an`| `ss -tuln`         | View connections |
| `nslookup`   | `dig`, `nslookup`  | DNS lookup       |

### Core Commands Reference

| Command      | Purpose           | Example                    |
| ------------ | ----------------- | -------------------------- |
| `ip addr`    | Show IP addresses | `ip addr show`             |
| `ip route`   | Show routing      | `ip route`                 |
| `ping -c 4`  | Test connectivity | `ping -c 4 google.com`    |
| `traceroute` | Trace path        | `traceroute google.com`    |
| `ss -tuln`   | Listening ports   | `ss -tuln`                 |
| `dig`        | DNS lookup        | `dig google.com`           |
| `curl`       | HTTP request      | `curl https://example.com` |
| `wget`       | Download file     | `wget URL`                 |
| `nc -zv`     | Test port         | `nc -zv host 80`           |

### Challenges:
---

**Challenge 5.1: View Network Configuration**

_Solution:_
```bash
ip addr show
ip route
cat /etc/resolv.conf
```
- `ip addr show` – Displays all network interfaces on the system along with their IP addresses and status.

- `ip route` – Shows the routing table, telling the system where to send network traffic.

- `cat /etc/resolv.conf` – Prints the DNS configuration, showing which servers are used to resolve domain names.
---

**Challenge 5.2: Test Connectivity**

_Solution:_
```bash
ping -c 4 8.8.8.8      # By IP (tests network)
ping -c 4 google.com   # By name (tests DNS too)
traceroute google.com
```

---

**Challenge 5.3: Check Listening Services**

_Solution:_
```bash
ss -tuln                    # All listening ports
sudo ss -tulnp             # Include process names
ss -tuln | grep :22        # Check specific port
```

---

**Challenge 5.4: DNS Lookups**

_Solution:_
```bash
dig google.com
dig +short google.com
nslookup google.com
```
Your local DNS resolver for the IPv4 addresses of google.com will likely return six different IPs (used for load balancing), quickly, via your local DNS stub.

---

**Challenge 5.5: Download Files**

_Solution:_
```bash
wget https://example.com/file
curl -O https://example.com/file
curl -I https://google.com  # Just headers
```

`wget`	Won’t save a file if server returns 404
`curl`	Saves whatever the server sends, even an error page

---

