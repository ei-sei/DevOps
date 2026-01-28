
## Table of Contents

1. [OSI & TCP/IP Models](#1-osi--tcpip-models)
2. [IP Addressing & Subnetting](#2-ip-addressing--subnetting)
3. [Key Protocols](#3-key-protocols)
4. [DNS (Domain Name System)](#4-dns-domain-name-system)
5. [DHCP (Dynamic Host Configuration Protocol)](#5-dhcp-dynamic-host-configuration-protocol)
6. [Routing Fundamentals](#6-routing-fundamentals)
7. [Firewalls & Security Groups](#7-firewalls--security-groups)
8. [NAT & Port Forwarding](#8-nat--port-forwarding)
9. [Load Balancing](#9-load-balancing)
10. [Container Networking](#10-container-networking)
11. [Cloud Networking (AWS/Azure/GCP)](#11-cloud-networking-awsazuregcp)
12. [Troubleshooting Tools & Commands](#12-troubleshooting-tools--commands)
13. [Common DevOps Networking Scenarios](#13-common-devops-networking-scenarios)

---

## 1. OSI & TCP/IP Models

### 1.1 The OSI Model (7 Layers)

_Why it matters in DevOps: Helps you identify WHERE a problem is occurring when troubleshooting._

| Layer | Name         | Example Protocols/Devices   | What It Does |
| ----- | ------------ | --------------------------- | ------------ |
| 7     | Application  | HTTP, DNS                   |              |
| 6     | Presentation | SSL/TLS                     |              |
| 5     | Session      | RTP                         |              |
| 4     | Transport    | TCP/UDP                     |              |
| 3     | Network      | IP                          |              |
| 2     | Data Link    | Ethernet, PPP               |              |
| 1     | Physical     | Copper cables, fibre optics |              |

**mnemonic:**
>Please Do Not Throw Sausage Pizza Away

### 1.2 The TCP/IP Model (4 Layers)

_This is what's actually used in practice._

| Layer       | OSI Equivalent                     | What It Does                                                                                                                                                                                                                                                                                                                                                                                                           | Key Protocols |
| ----------- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| Application | Session, Presentation, Application | HTTP provides an interface between the software running on the computer and the network itself. This is used to define the services that an application needs. For example, HTTP defines how web browsers can pull the contents of a web page from a web server.                                                                                                                                                       | HTTP          |
| Transport   | Transport                          | The Transport Layer decides _how_ data gets from A to B. TCP guarantees reliable, ordered delivery with error-checking; good for SSH, databases, anything that needs accuracy. UDP skips those checks and reorders packets without caring, making it fast; used for VoIP, video streaming, online gaming where speed matters more than perfection. It also manages port numbers so data reaches the right application. | TCP/UDP       |
| Internet    | Network                            | The Internet Layer routes data across different networks using IP addresses. Routers read the destination IP and forward packets along the best path to reach it. It's also responsible for fragmentation (splitting large packets) and diagnostics like ping. IPv4 still dominates, but IPv6 is gradually replacing it.                                                                                               | IP            |
| Link        | Data link, Physical                | The Data Link Layer handles communication between devices on the same local network (LAN) using Ethernet. It uses MAC addresses, unique identifiers burned into network interfaces, to deliver frames to the correct physical device. MAC addresses don't need configuration; they're set at manufacture. Switches operate at this layer.                                                                              | Ethernet, PPP |

### 1.3 How Data Flows (Encapsulation)

**What happens when you visit a website:**

1. Application layer: Browser sends HTTP request to www.example.com (port 80 or port 443 for HTTPS)
2. Transport layer: TCP connection is established (three-way handshake on port 80). Data split into segments with source/destination ports attached
3. Network layer: IP packet created with destination IP address (e.g. 93.184.216.34). Routers forward the packet across networks using route tables.
4. Data link layer: Frames converted to Ethernet with destination MAC address. Switch delivers frames to the correct physical port on the local network.

**DevOps Application:**
> When would understanding layers help you troubleshoot? Give an example:
```
Example: Your health check to a load balancer keeps timing out.

	- Layer 7 (Application): Is the health check using the right protocol/port?        (HTTP vs HTTPS?)
	  
	- Layer 4 (Transport): Is the target allowing traffic on the port? (security       group rule blocking it?)
	
	- Layer 3 (Network): Can the load balancer reach the target network? (route        table misconfigured?)
	  
	- Layer 2 (Data Link): Is the target connected to the netwrok? (NIC down?)
	
You would test from top down: `curl` to check Layer 7 -> `ss -tulnp` to check Layer 4 -> `ping` to check Layer 3
```


---

## 2. IP Addressing & Subnetting

### 2.1 IPv4 Basics

**What is an IP address?**
> A unique identifier for a device on a network

**Structure of IPv4:**
- Total bits: 32
- Format: 4 Octets, each octet = 8 bits
- Example: 192.168.1.1

**Public vs Private IP Addresses:**

| Type              | Purpose                                                    | Ranges                                           |
| ----------------- | ---------------------------------------------------------- | ------------------------------------------------ |
| Public            | Routable on the internet; devices can communicate globally | Any IP not in the private/loopback ranges        |
| Private (Class A) | Internal networks; not routable on the internet            | 10.0.0.0 to 10.255.255.255                       |
| Private (Class B) | Internal networks; not routable on the internet            | 172.16.0.0 to 172.31.255.255                     |
| Private (Class C) | Internal networks; not routable on the internet            | 192.168.0.0 to 192.168.255.255                   |
| Loopback          | Local machine communication; always points to itself       | 127.0.0.0 to 127.255.255.255 (usually 127.0.0.1) |
> **Note:** Loopback is a virtual network interface that talks to itself. Traffic sent to 127.0.0.1 never leaves your machine. Useful for testing network services locally without needing a real network. Used by applications to communicate internally. Always works; no network card, cables or internet needed.

### 2.2 Subnet Masks

**What is a Subnetting?**
> A method to divide a larger network into smaller, more manageable sub-networks or subnets. This is done by borrowing bits from the host portion of an IP address to create additional network bits.

**What is Subnet Masks?**
> A 32 bit number used to divide an IPv4 address into a network portion and host portion.

**Common subnet masks:**

| CIDR | Subnet Mask     | Usable Hosts | Use Case                             |
| ---- | --------------- | ------------ | ------------------------------------ |
| /8   | 255.0.0.0       | 16,777,214   | Huge networks (rarely used)          |
| /16  | 255.255.0.0     | 65,534       | Large enterprise networks            |
| /24  | 255.255.255.0   | 254          | Standard subnet (most common in AWS) |
| /26  | 255.255.255.192 | 64           | Dividing /24 into smaller subnets    |
| /28  | 255.255.255.240 | 14           | Small subnets, tight spaces          |
| /29  | 255.255.255.248 | 6            | Point-to-point links, VPN tunnels    |
| /30  | 255.255.255.252 | 2            | Router-to-router connections         |
| /31  | 255.255.255.254 | 2            | Point-to-point (no broadcast)        |
| /32  | 255.255.255.255 | 1            | Single host (route to one IP)        |

### 2.3 CIDR Notation

**What is CIDR?**

> Classless Inter-Domain Routing - A shorthand way to write an IP address and its subnet mask together. 

**How to read 10.0.1.0/24:**

- Network portion: 10.0.1.0 (first 24 bits)
- Host portion: Last 8 bits (the .0 to .255 range)
- Number of addresses: 256 (2^8)
- Usable addresses: 254 (256 minus network address 10.0.1.0 and broadcast 10.0.1.255)

### 2.4 Subnetting Practice

**Example: Subnet 192.168.1.0/24 into 4 equal subnets**

| Subnet | Network Address  | Usable Range                  | Broadcast     |
| ------ | ---------------- | ----------------------------- | ------------- |
| 1      | 192.168.1.0/26   | 192.168.1.1 - 192.168.1.62    | 192.168.1.63  |
| 2      | 192.168.1.64/26  | 192.168.1.65 - 192.168.1.126  | 192.168.1.127 |
| 3      | 192.168.1.128/26 | 192.168.1.129 - 192.168.1.190 | 192.168.1.191 |
| 4      | 192.168.1.192/26 | 192.168.1.193 - 192.168.1.254 | 192.168.1.255 |

**New subnet mask:** 255.255.192
```
How it works:
- Original /24 = 256 addresses
- Divide by 4 = 64 addresses per subnet
- /24 + 2 bits = /26 (each subnet)
- Each subnet gets 62 usable IPs (64 - 2 for network/broadcast)

DevOps context: This is how you'd split a VPC into multiple subnets — public subnet for web servers, private for databases, etc.
```

### 2.5 IPv6 Basics

**Why IPv6 exists:**

> IPv4 only has 4.3 billion addresses, which the internet has mostly run out. IPv6 has 340 undecillion addresses (basically unlimited).

**IPv6 format:**

- Total bits: 128
- Format: 8 groups of 4 hexadecimal digits separated by colons. Each group = 16 bits.
- Example: 2001:0db8:85a3:0000:0000:8a2e:0370:7334

**DevOps Application:**

> How does subnetting apply when creating AWS VPCs?
> **AWS VPCs:**
> 	- You define a VPC with a CIDR block (e.g., 10.0.0.0/16)
> 	- Subnet it into smaller /24s for different tiers (10.0.1.0/24 for web, 10.0.2.0/24 for database)
> 	- Public subnets get internet access via Internet Gateway; private subnets don't
> 	- Security groups and NACLs control traffic _between_ subnets
> 	- Each subnet needs a route table pointing where traffic goes

---

## 3. Key Protocols

### 3.1 TCP (Transmission Control Protocol)

**What it is:**
> A reliable, connection-based protocol that guarantees data arrives in order and without errors.

**Key characteristics:**
- Connection type: Connection-oriented (establishes handshake before sending data)
- Reliability: Guaranteed delivery, ordered, error-checking (re-transmits lost segments)
- Use cases: Web (HTTP/HTTPS), SSH, databases, email, file transfers, anything needing accuracy

**The TCP 3-Way Handshake:**
1. SYN: Client sends synchronisation packet to server saying "I want to connect"
2. SYN-ACK: Server receives SYN, sends back synchronisation-acknowledgement saying "I got it, I'm ready"
3. ACK: Client receives SYN-ACK, sends acknowledgement back saying "Connection established"

**Common TCP ports:**

| Port | Service     | What It's Used For                               |
| ---- | ----------- | ------------------------------------------------ |
| 22   | SSH         | Remote terminal access, secure command execution |
| 80   | HTTP        | Unencrypted web traffic                          |
| 443  | HTTPS       | Encrypted web traffic (HTTP + TLS/SSL)           |
| 3306 | MySQL       | Database queries and connections                 |
| 5432 | PostgresSQL | Database queries and connections                 |
**DevOps context:** When you configure security groups in AWS, you open these ports. SSH (22) for admin access, HTTP/HTTPS (80/443) for web servers, database ports (3306/5432) for app-to-database communication.

### 3.2 UDP (User Datagram Protocol)

**What it is:**
> A fast, connectionless protocol that sends data without guaranteeing delivery or order.

**Key characteristics:**

- Connection type: Connectionless (sends data immediately, no handshake)
- Reliability: Best-effort delivery, no guaranteed order, no error-checking or retransmission
- Use cases: DNS, video streaming, online gaming, VoIP, live broadcasts, anything prioritising speed over accuracy

**Common UDP ports:**

| Port  | Service | What It's Used For                                  |
| ----- | ------- | --------------------------------------------------- |
| 53    | DNS     | Domain name resolution (translate domain to IP)     |
| 67/68 | DHCP    | Assigning IP addresses to devices automatically     |
| 123   | NTP     | Network Time Protocol (synchronising system clocks) |

### 3.3 TCP vs UDP Comparison

| Feature     | TCP                                          | UDP                                |
| ----------- | -------------------------------------------- | ---------------------------------- |
| Connection  | Connection-oriented (handshake required)     | Connectionless (no setup)          |
| Reliability | Guaranteed delivery, ordered, error-checking | Best-effort, no guarantees         |
| Speed       | Slower (due to acknowledgements)             | Faster (no overhead)               |
| Overhead    | Higher (sequence numbers, retransmission)    | Lower (minimal headers)            |
| Use when    | Accuracy matters (web, SSH, databases)       | Speed matters (DNS, video, gaming) |

### 3.4 HTTP/HTTPS

**HTTP:**
> An application-layer protocol for transferring web pages and data over the internet. Unencrypted; anyone can read the traffic.

**HTTPS:**
> HTTP wrapped in TLS/SSL encryption. Data is encrypted; traffic is unreadable to eavesdroppers.

**Common HTTP methods:**

| Method | Purpose                                      | Idempotent? |
| ------ | -------------------------------------------- | ----------- |
| GET    | Retrieve data from server                    | Yes         |
| POST   | Submit data to server (creates new resource) | No          |
| PUT    | Replace entire resource                      | Yes         |
| DELETE | Remove resource                              | Yes         |
| PATCH  | Partially update resource                    | Yes         |

**HTTP status codes to know:** https://http.cat/

| Code | Meaning               | When You See It                                       |
| ---- | --------------------- | ----------------------------------------------------- |
| 200  | OK                    | Request succeeded, server returned data               |
| 201  | Created               | Resource successfully created (POST request)          |
| 301  | Moved Permanently     | URL permanently redirected (old link → new link)      |
| 400  | Bad Request           | Client sent malformed request (syntax error)          |
| 401  | Unauthorised          | Authentication required (missing/invalid credentials) |
| 403  | Forbidden             | Authenticated but not allowed (permission denied)     |
| 404  | Not Found             | Resource doesn't exist                                |
| 500  | Internal Server Error | Server crashed or unexpected error                    |
| 502  | Bad Gateway           | Load balancer can't reach backend server              |
| 503  | Service Unavailable   | Server overloaded or temporarily down                 |
**DevOps context:**
- **200** = healthy (load balancer health checks expect this)
- **5xx errors** = your problem (app/server issue)
- **502** = backend down (check if instances are running)
- **503** = too much traffic (scale up or check if service crashed)
-
### 3.5 SSH

**What it is:**

> A secure protocol for remotely accessing and controlling servers over an encrypted connection.

**Default port:** 22

**Key-based vs password authentication:**

> Passwords are human memorable (weak). Keys are cryptographically strong. Attackers can not guess a 2048-bit RSA key.

**DevOps Application:**
```
- Launch EC2 instance → AWS gives you a key pair
- SSH into instance to configure it: `ssh -i mykey.pem ec2-user@instance-ip`
- Deploy code, install packages, check logs
- Automate with Ansible/Terraform (uses SSH in background)
- Configure bastion host (jump server) to access private instances through public one
- SCP files to/from servers: `scp -i mykey.pem file.txt user@server:/path/`


**Security checklist:**

- Key permissions: `chmod 400 mykey.pem` (only you can read)
- Security group allows port 22 from your IP only (not 0.0.0.0)
- Disable password auth on servers (force keys only)
- Rotate keys regularly
```

---

## 4. DNS (Domain Name System)

### 4.1 What DNS Does

**In simple terms:**

> Translates human-readable domain names (google.com) into IP addresses (142.250.80.46) so your browser can connect to the right server.

**Analogy:**

> DNS is the internet's phone book. You know someone's name (google.com) but need their phone number (IP address) to call them. You look it up in the directory, get the number, and dial. If you call them often, you remember the number (cache). If you don't know it, you look it up again.

### 4.2 DNS Record Types

| Type  | Purpose                                     | Example                                                 |
| ----- | ------------------------------------------- | ------------------------------------------------------- |
| A     | Maps domain to IPv4 address                 | example.com → 93.184.216.34                             |
| AAAA  | Maps domain to IPv6 address                 | example.com → 2001:0db8:85a3::8a2e:0370:7334            |
| CNAME | Alias (points domain to another domain)     | [www.example.com](http://www.example.com) → example.com |
| MX    | Mail server for the domain                  | example.com mail goes to mail.example.com               |
| TXT   | Text records (verification, SPF, DKIM)      | v=spf1 include:_spf.google.com                          |
| NS    | Nameserver (which server holds DNS records) | ns1.example.com is authoritative for example.com        |
| PTR   | Reverse DNS (IP to domain)                  | 93.184.216.34 → example.com                             |
| SRV   | Service location (ports, priorities)        | _sip._tcp.example.com → server:port                     |

### 4.3 DNS Resolution Process

**What happens when you visit www.example.com:**

1. Browser checks: Its own cache (recently visited domains)
2. OS checks: Operating system cache (host file, resolver cache)
3. Query goes to: Recursive resolver
4. Recursive resolver: Checks its cache; if not found, starts querying authoritative servers
5. Root server: Responds "I don't know example.com, but ask the .com TLD server"
6. TLD server: Responds "I don't know example.com, but ask the authoritative nameserver at ns1.example.com"
7. Authoritative server: Responds "[www.example.com](http://www.example.com) = 93.184.216.34"
8. Response: Resolver caches answer, sends back to browser. Browser connects to 93.184.216.34

### 4.4 DNS Caching & TTL

**What is TTL?**

> **TTL** (Time To Live): A number (in seconds) that tells DNS caches how long to keep a DNS record before fetching it again.

**Why caching matters:**

> DNS answers are served instantly from cache instead of querying servers every time, making lookups fast and reducing load on DNS infrastructure.

### 4.5 Common DNS Tools

| Tool     | Command Example        | What It Shows                                                              |
| -------- | ---------------------- | -------------------------------------------------------------------------- |
| nslookup | `nslookup example.com` | IP address for domain (simple, older tool)                                 |
| dig      | `dig example.com`      | Detailed DNS response (record type, TTL, query time, authoritative server) |
| host     | `host example.com`     |                                                                            |

**DevOps Application:**
>**Scenario:** You deployed a new load balancer and updated DNS to point to its new IP, but users still see the old website.

**Troubleshooting steps:**

1. **Check your DNS record:**
```dig yourdomain.com```
Does it show the new load balancer IP? If not, the DNS update didn't apply yet.

2. **Check TTL:**
```dig yourdomain.com | grep "yourdomain"```
If TTL is high (86400), old cached answers will persist for 24 hours. Old resolvers still have the old IP cached.

3. **Flush your local cache:**
```
# Linux
sudo systemctl restart systemd-resolved
```

4. **Test with different resolvers:**
```bash
dig @8.8.8.8 yourdomain.com
dig @1.1.1.1 yourdomain.com
```

Different resolvers might have different cached answers. Google (8.8.8.8) and Cloudflare (1.1.1.1) caches refresh faster.

5. **Check propagation:** Use online tools like whatsmydns.net to see if DNS has propagated globally.

6. **If still wrong after 24 hours:**
	- Verify you updated the correct DNS record in Route 53
	- Check that authoritative nameserver (NS record) is correct
	- Confirm the load balancer IP is correct

**Lesson:** Always lower TTL _before_ changing DNS to speed up propagation.



---

## 5. DHCP (Dynamic Host Configuration Protocol)

### 5.1 What DHCP Does

**In simple terms:**
> A protocol that automatically assigns IP addresses and network configuration to devices on a network. No manual setup needed.

### 5.2 The DORA Process

| Step | Name        | What Happens                                                        |
| ---- | ----------- | ------------------------------------------------------------------- |
| D    | Discover    | Client broadcasts "I need an IP" to all DHCP servers on the network |
| O    | Offer       | DHCP server responds "I can give you IP 192.168.1.50"               |
| R    | Request     | Client broadcasts "I accept that offer" (confirms to all servers)   |
| A    | Acknowledge | DHCP server sends final confirmation and lease details              |

### 5.3 DHCP Lease

**What is a lease?**
> A time-limited assignment of an IP address. The server "lends" the IP to a device for a set duration (hours to days). When the lease expires, the IP goes back to the pool.

**Lease renewal process:**
> Device's DHCP lease is halfway through its duration. Device sends renewal request to same DHCP server asking to extend the lease. Server responds with new expiration time (usually another full lease period). Device now has more time before IP expires. If server doesn't respond, device waits until 87.5% of lease time, then broadcasts to _any_ DHCP server asking for renewal (rebind). Once renewed, lease timer resets and process repeats.

### 5.4 Static vs Dynamic IP

| Type    | Pros                                             | Cons                                  | Use When                                                             |
| ------- | ------------------------------------------------ | ------------------------------------- | -------------------------------------------------------------------- |
| Static  | Predictable, doesn't change, easy to reference   | Manual setup, requires admin overhead | Servers, databases, load balancers, anything needing a fixed address |
| Dynamic | Automatic assignment, no manual config, flexible | IP can change, harder to reference    | Clients (laptops, phones), temporary devices, development            |

**DevOps Application:**
> When would you use static IPs in cloud infrastructure?
> 3-tier app, load balancer gets static IP (DNS points to it), app servers use dynamic IPs (load balancer routes to them), database gets static IP (app servers know where to find it).

---

## 6. Routing Fundamentals

### 6.1 What Routing Is

**In simple terms:**
> The process of forwarding data packets from source to destination across networks. Routers decide the best path based on destination IP address.

### 6.2 Routing Table

**What a routing table contains:**
> A routing table is a set of rules (entries) that tells the router where to send packets based on destination IP. Each entry specifies: "If destination matches this network, send to this gateway/interface."

**Example routing table entry:**
```
Destination: 10.0.2.0/24 
Gateway: 10.0.1.1 
Interface: eth0 
Metric: 100
```

**How to view routing table:**
- Linux: `ip route show`
- Windows: `route print`

### 6.3 Default Gateway

**What it is:**
> The router sends packets to when the destination IP is on a different network (not local).

**When it's used:**
> Anytime traffic leaves your local subnet

### 6.4 Static vs Dynamic Routing

| Type    | How It Works                                                                                | Pros                                              | Cons                                                       |
| ------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------- | ---------------------------------------------------------- |
| Static  | Admin manually creates routing table entries                                                | Predictable, low overhead, secure (no surprises)  | Doesn't adapt to network changes, manual updates required  |
| Dynamic | Routers communicate with each other to discover best paths (using protocols like OSPF, BGP) | Automatically adapts to network outages, scalable | More complex, higher CPU/bandwidth, harder to troubleshoot |

### 6.5 Key Routing Concepts

**Hop:**
> A single step in a packet's journey from source to destination. Each router the packet passes through = one hop. Traceroute shows the number of hops to reach a destination.

**Metric:**
> A numerical value routers use to rank routing options. Lower metric = preferred route. Metrics can be based on: hop count, bandwidth, latency, reliability. If multiple routes exist to the same destination, router picks the one with lowest metric.

**Longest prefix match:**
> When multiple routes match a destination IP, use the most specific one (longest CIDR prefix). Example: If routing table has both 10.0.0.0/8 and 10.0.1.0/24, traffic to 10.0.1.50 uses 10.0.1.0/24 because it's more specific.

**DevOps Application:**
> How does routing apply to AWS VPCs and route tables?
> Each subnet has a route table defining where traffic goes:
> Example routes:
> 	10.0.0.0/16 (local) → Local (stay in VPC)
> 	0.0.0.0/0 (anywhere else) → Internet Gateway (go to internet)
> 	10.1.0.0/16 (different VPC) → VPC Peering Connection
> 	0.0.0.0/0 (for private subnet) → NAT Gateway (outbound only)



---

## 7. Firewalls & Security Groups

### 7.1 What a Firewall Does

**In simple terms:**
> A security device/software that filters network traffic based on rules. It decides which packets are allowed through and which are blocked.

### 7.2 Stateful vs Stateless

| Type      | How It Works                                                                                                                                      | Example                                                                                                  |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Stateful  | Remembers established connections. If outbound traffic is allowed, inbound response is automatically allowed (even without explicit inbound rule) | Allow outbound to 8.8.8.8:53 (DNS). Response automatically allowed back in without separate inbound rule |
| Stateless | Checks each packet independently. Inbound and outbound rules are separate; must explicitly allow both directions                                  | Allow outbound on port 443. Must also explicitly allow inbound on port 443 for responses to return       |

### 7.3 Firewall Rules

**Basic rule components:**

- Source: Where traffic originates (IP address or CIDR range, e.g., 192.168.1.0/24 or 0.0.0.0/0 for anywhere)
- Destination: Where traffic is going (IP address or CIDR range, e.g., 10.0.1.50 or 10.0.0.0/16)
- Port: Layer 4 port number (e.g., 22 for SSH, 443 for HTTPS, or port range 8000-9000)
- Protocol: Transport layer protocol (TCP, UDP, ICMP, or all)
- Action: Allow or Deny the traffic

**Rule processing order:**
> Rules are evaluated **top-to-bottom, first match wins**. When traffic arrives, the firewall checks each rule in sequence:
> 

**DevOps context:** 
> In AWS Security Groups, rules are evaluated but order doesn't matter much (all allow rules are combined). In NACLs, order is critical — must number rules 100, 110, 120, etc. and order them carefully.

### 7.4 AWS Security Groups

**What they are:**
>Stateful firewalls attached to EC2 instances (and other AWS resources). They control inbound and outbound traffic at the instance level.

**Key characteristics:**
- State: Stateful
- Default inbound: Deny all (blocks everything unless you explicitly allow)
- Default outbound: Allow all (permits all outbound traffic by default)

**Example security group rules for a web server:**

| Type     | Protocol | Port | Source    | Purpose                                       |
| -------- | -------- | ---- | --------- | --------------------------------------------- |
| Inbound  | TCP      | 80   | 0.0.0.0/0 | Allow HTTP traffic from anywhere              |
| Inbound  | TCP      | 443  | 0.0.0.0/0 | Allow HTTPS traffic from anywhere             |
| Outbound | TCP      | 443  | 0.0.0.0/0 | Allow outbound HTTPS (for external API calls) |

### 7.5 Network ACLs (NACLs)

**What they are:**
>**NACLs** (Network Access Control Lists): Stateless firewalls at the subnet level. They filter traffic entering and leaving a subnet before it reaches instances.

**Security Groups vs NACLs:**

| Feature   | Security Group                        | NACL                                                       |
| --------- | ------------------------------------- | ---------------------------------------------------------- |
| Level     | Instance-level                        | Subnet-level                                               |
| Stateful? | Yes (stateful)                        | No (stateless)                                             |
| Rules     | Order doesn't matter; all rules apply | Order matters; numbered (100, 110, etc.), first match wins |
| Default   | Deny inbound, allow outbound          | Allow all inbound/outbound (you add deny rules)            |

**DevOps Application:**
>DevOps Application: Security for a 3-Tier Application

**Architecture:**
```
Internet → Load Balancer (Public Subnet)
           ↓
        Web Tier (Public Subnet)
           ↓
        App Tier (Private Subnet)
           ↓
        Database Tier (Private Subnet)
```

**Security Group Rules:**
***Load Balancer Security Group:***
```
Inbound:
  - TCP 80 from 0.0.0.0/0 (HTTP from anywhere)
  - TCP 443 from 0.0.0.0/0 (HTTPS from anywhere)

Outbound:
  - TCP 80 to web-tier-sg (forward to web servers)
  - TCP 443 to web-tier-sg (forward to web servers)
```

**Web Tier Security Group:**
```
Inbound:
  - TCP 80 from load-balancer-sg (only from LB)
  - TCP 443 from load-balancer-sg (only from LB)

Outbound:
  - TCP 443 to app-tier-sg (call app servers)
```

**App Tier Security Group:**
```
Inbound:
  - TCP 8080 from web-tier-sg (only from web servers)

Outbound:
  - TCP 3306 to database-tier-sg (query database)
  - TCP 443 to 0.0.0.0/0 (external APIs if needed)
```

**Database Tier Security Group:**
```
Inbound:
  - TCP 3306 from app-tier-sg (only from app servers)

Outbound:
  - None needed (databases don't initiate outbound)
```

**Why this works:**
- **Defense in depth:** Each tier only talks to the tier it needs
- **Least privilege:** No unnecessary ports open
- **No direct internet access:** Private subnets (app/db) can't be reached from internet
- **Stateful:** Responses automatically allowed back (no manual allow rules needed)

**Optional NACL layer:** Add NACLs to each subnet to deny specific malicious IPs or block entire ranges at subnet boundary (extra security, rarely needed for this setup).


---

## 8. NAT & Port Forwarding

### 8.1 What NAT Is

**In simple terms:**
> A technique that translates private IP addresses to public IP addresses (and vice versa). Lets devices with private IPs communicate with the internet.

**Why NAT exists:**
> NAT lets multiple private devices share a single public IP while hiding them from direct internet access (security + address efficiency).

### 8.2 Types of NAT

| Type                           | What It Does                                                            | Use Case                                                                         |
| ------------------------------ | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Static NAT                     | Maps one private IP to one public IP permanently (1:1)                  | Web servers, mail servers need consistent public IP                              |
| Dynamic NAT                    | Maps private IPs to public IPs from a pool (many private to many public | Multiple servers sharing a range of public IPs                                   |
| PAT (Port Address Translation) | Maps many private IPs to one public IP using different ports (many:1)   | Home/office networks, AWS NAT Gateway; hundreds of devices share one public IP\| |

### 8.3 NAT Gateway (AWS)

**What it does:**
> NAT Gateway is an AWS service that lets private instances initiate outbound connections to the internet while blocking inbound connections from the internet.

**When you need it:**
> You need a NAT Gateway when private instances need to initiate outbound connections to the internet (download packages, call external APIs, reach databases outside VPC) but should never be reachable from the internet.

**NAT Gateway vs NAT Instance:**

| Feature      | NAT Gateway                     | NAT Instance                                     |
| ------------ | ------------------------------- | ------------------------------------------------ |
| Managed      | AWS managed (fully)             | You manage (patch, maintain)                     |
| Availability | Highly available, auto-failover | Single point of failure (must manage redundancy) |
| Cost         | Hourly + per GB processed       | EC2 instance cost only                           |
| Performance  | High throughput, optimised      | Limited by instance size                         |
| Setup        | Create and done                 | Launch instance, configure software              |

### 8.4 Port Forwarding

**What it is:**
> Port Forwarding is a NAT technique that redirects incoming traffic on one port to a different port on another device (usually on a private network).

**Example scenario:**
```
1. External traffic arrives at public IP on port X
2. Port forwarding rule intercepts it
3. Traffic is redirected to private IP on port Y
4. Private device receives traffic on port Y
5. Response goes back through the same path
```

**DevOps Application:**
> How does NAT apply to private subnets in AWS?
> 	Less common in modern cloud (AWS uses Security Groups and load balancers instead). More typical for on-premises networks or home lab setups. Kubernetes Ingress controllers use similar concepts to route traffic.

---

## 9. Load Balancing

### 9.1 What Load Balancing Does

**In simple terms:**
> Load Balancing distributes incoming traffic across multiple servers so no single server gets overwhelmed. It acts as a traffic director, sending each request to the least busy server.
```
**How it works:**

1. Client sends request to load balancer (single entry point)
2. Load balancer checks health of backend servers
3. Load balancer picks the best server (based on algorithm: round-robin, least connections, etc.)
4. Request is forwarded to that server
5. Server responds through load balancer back to client
```

**Why it's needed:**
> 1. **Scalability:** Handle more traffic by adding more servers instead of upgrading one big server
> 2. **High availability:** If one server fails, load balancer routes traffic to healthy servers (zero downtime)
> 3. **Performance:** Distribute load evenly so no server becomes a bottleneck
> 4. **Redundancy:** Multiple copies of your service running simultaneously

### 9.2 Types of Load Balancers

| Type             | OSI Layer             | What It Balances                              | Example                                                                            |
| ---------------- | --------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------- |
| L4 (Network)     | Layer 4 (Transport)   | TCP/UDP traffic by port and IP                | AWS Network Load Balancer (NLB), distributes based on protocol/port                |
| L7 (Application) | Layer 7 (Application) | HTTP/HTTPS requests by URL, hostname, headers | AWS Application Load Balancer (ALB), routes /api to one server, /images to another |

### 9.3 Load Balancing Algorithms

| Algorithm         | How It Works                                                                                              | Best For                                                    |
| ----------------- | --------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Round Robin       | Sends each request to the next server in order (server 1, 2, 3, 1, 2, 3...)                               | Simple workloads with equal server capacity                 |
| Least Connections | Sends request to server with fewest active connections                                                    | Long-lived connections (WebSockets, database pools)         |
| IP Hash           | Uses client IP to determine which server (same client always goes to same server)                         | Session persistence without sticky sessions                 |
| Weighted          | Assigns weights to servers; higher weight gets more traffic (server 1: 50%, server 2: 30%, server 3: 20%) | Servers with different capacity (one beefy, others smaller) |

### 9.4 Health Checks

**What they are:**
> Health Checks are periodic tests the load balancer runs on backend servers to verify they're alive and responding correctly. If a server fails, the load balancer stops sending traffic to it.
```
**How it works:**

1. Load balancer sends health check request to each backend server (e.g., HTTP GET to /health endpoint)
2. Server responds (typically 200 OK)
3. Load balancer marks server as healthy
4. Process repeats every N seconds (configurable)
5. If server doesn't respond or returns error, marked unhealthy
```

**What happens when a server fails health check:**
> 1. Load balancer immediately stops routing new requests to that server
> 2. Existing connections drain (graceful shutdown if configured)
> 3. Traffic redistributes to remaining healthy servers
> 4. Monitoring/alerting triggers (optional, depends on setup)
> 5. Server is removed from the load balancer pool
> 6. If server recovers (passes health check again), it's added back automatically

### 9.5 AWS Load Balancers

| Type              | Layer     | Use Case                                                                                |
| ----------------- | --------- | --------------------------------------------------------------------------------------- |
| ALB (Application) | Layer 7   | Web apps, microservices, hostname/path-based routing (modern standard)                  |
| NLB (Network)     | Layer 4   | Ultra-high performance, extreme throughput, non-HTTP protocols (gaming, IoT, databases) |
| CLB (Classic)     | Layer 4/7 | Legacy (older applications, not recommended for new projects)                           |
**ALB (Application Load Balancer):**
- Routes based on: hostname, URL path, HTTP headers, query parameters
- Example: Route api.example.com to API servers, [www.example.com/images](http://www.example.com/images) to image servers
- Best for: Kubernetes, Docker, microservices
- Cost: Mid-range

**NLB (Network Load Balancer):**
- Extreme throughput (millions of requests per second)
- Low latency (microseconds)
- Supports: TCP, UDP, TLS protocols
- Best for: Gaming, real-time applications, extreme scale
- Cost: Higher

**CLB (Classic Load Balancer):**
- Old generation, still works but outdated
- Less flexible routing than ALB
- Avoid for new projects (AWS prefers ALB/NLB)

**DevOps Context:**
> Use ALB for 99% of web applications. Use NLB only if you need extreme performance or non-HTTP protocols. CLB is legacy; don't bother learning it.

---

## 10. Container Networking

### 10.1 Docker Networking Basics

**How containers communicate:**
> Containers don't have real network interfaces by default. Docker creates virtual networks that isolate containers while letting them talk to each other and the host.
```
**How it works:**

1. Docker creates a bridge network (virtual switch) on the host
2. Each container gets a virtual network interface (veth)
3. Container is assigned an IP from the bridge subnet (e.g., 172.17.0.2)
4. Containers on same network can ping/connect using IP or container name (DNS)
5. Traffic between containers flows through the bridge
6. NAT translates between container and host network
```
### 10.2 Docker Network Types

| Type    | What It Does                                                                          | Use Case                                                                          |
| ------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| bridge  | Default network. Containers get isolated IP addresses, communicate via virtual bridge | Single-host applications, development, internal container communication           |
| host    | Container shares host network (no isolation). Uses host's IP and ports directly       | High-performance applications, need direct host access, single container per port |
| none    | Container has no network access (isolated completely)                                 | Security, testing, containers that don't need networking                          |
| overlay | Multi-host network spanning Docker Swarm/Kubernetes nodes                             | Swarm mode, Kubernetes, distributed applications across multiple hosts            |

### 10.3 Docker Network Commands

| Command                  | What It Does                                                              |
| ------------------------ | ------------------------------------------------------------------------- |
| `docker network ls`      | List all Docker networks on the host                                      |
| `docker network create`  | Create a new custom network                                               |
| `docker network inspect` | View detailed info about a network (IP range, connected containers, etc.) |
| `docker network connect` | Connect a running container to a network                                  |

### 10.4 Container-to-Container Communication

**Same network:**
> Containers on the same Docker network can communicate directly by container name or IP address.
```
**How it works:**

1. Container A sends request to container-b (or 172.17.0.3)
2. Docker's embedded DNS resolver translates container name to IP
3. Traffic flows through the bridge network
4. Container B receives and responds
5. Reply goes back to Container A
```

**Different networks:**
> Containers on different networks cannot communicate directly by name or IP. They're isolated.
```
**To communicate, you need:**

1. Connect container to second network: `docker network connect network-2 container-name`
2. Expose and map ports through host (publish port on host, other container connects via host IP)
3. Use external DNS/service discovery (Kubernetes, Consul)
```


### 10.5 Publishing Ports

**What `-p 8080:80` means:**
> Maps host port 8080 to container port 80. External traffic reaching the host on port 8080 gets forwarded to the container's port 80.

**Difference between `-p` and `-P`:**
> `-p 8080:80`Explicitly map host port 8080 to container port 80
> `-P` (uppercase) Automatically map all exposed ports to random host ports

### 10.6 Kubernetes Networking

**Key concepts:**

| Concept        | What It Does                                                                                                    |
| -------------- | --------------------------------------------------------------------------------------------------------------- |
| Pod networking | Every pod gets its own IP address. Pods on same node communicate directly; cross-node uses overlay network      |
| Service        | Every pod gets its own IP address. Pods on same node communicate directly; cross-node uses overlay network      |
| ClusterIP      | Default service type. Exposes service only within cluster (internal IP). Other pods reach it by service name    |
| NodePort       | Exposes service on a port on every node. External traffic connects via node-ip:node-port                        |
| LoadBalancer   | Cloud provider creates external load balancer (e.g., AWS ELB). Exposes service to internet                      |
| Ingress        | Layer 7 load balancer. Routes HTTP/HTTPS traffic by hostname/path to services (more flexible than LoadBalancer) |

**DevOps Context:**
> ClusterIP for internal services (databases, caches). NodePort for testing/debug. LoadBalancer/Ingress for production external access. Ingress is preferred (more flexible, cheaper than multiple LoadBalancers).

---

## 11. Cloud Networking (AWS/Azure/GCP)

### 11.1 VPC (Virtual Private Cloud)

**What it is:**

> A VPC is an isolated virtual network within a cloud provider where you launch your cloud resources (servers, databases, load balancers). It's your own private piece of the cloud.

**Key components:**

- VPC: Isolated virtual network with CIDR block (e.g., 10.0.0.0/16). Everything else lives inside it.
- Subnet: Smaller network carved from VPC CIDR (e.g., 10.0.1.0/24). Resides in one Availability Zone. Can be public (has internet access) or private (doesn't).
- Route Table: Set of rules defining where traffic goes. Example: "0.0.0.0/0 → Internet Gateway" means all external traffic goes to the internet.
- Internet Gateway: Gateway connecting VPC to the internet. Attached to VPC. Public subnets route through it to reach external IPs.
- NAT Gateway: Translates private IPs to public IP for outbound internet access. Sits in public subnet. Private subnets route outbound traffic through it (but internet can't initiate connections back).

### 11.2 Public vs Private Subnets

| Type    | Has Route To                       | Use For                                                                             |
| ------- | ---------------------------------- | ----------------------------------------------------------------------------------- |
| Public  | Internet Gateway (0.0.0.0/0 → IGW) | Web servers, load balancers, bastion hosts, anything needing direct internet access |
| Private | NAT Gateway (0.0.0.0/0 → NAT)      | Databases, app servers, caches, anything that shouldn't be reachable from internet  |

### 11.3 VPC Peering

**What it is:**
> VPC Peering is a direct connection between two VPCs that allows resources in each VPC to communicate as if they're on the same network (using private IPs, no internet gateway needed).

**When to use it:**
> - **Multi-region applications:** VPC in us-east (app) peered with VPC in eu-west (data)
> - **Shared services:** Central VPC with shared databases/tools peered with multiple application VPCs
> - **Development/staging/production:** Separate VPCs for isolation, peered for cross-environment communication
> - **Organisation-wide networks:** Connect VPCs from different teams/departments

### 11.4 VPN & Direct Connect

**VPN:**
> VPN (Virtual Private Network) creates an encrypted tunnel between your on-premises network and your VPC over the internet. Traffic is encrypted end-to-end.

**Direct Connect / ExpressRoute:**
>Direct Connect (AWS) or ExpressRoute (Azure) is a dedicated physical network connection from your on-premises location to the cloud provider's data centre.

### 11.5 Availability Zones

**What they are:**
> Availability Zones (AZs) are physically separate data centres within a region, each with independent power, cooling, and networking. One region has multiple AZs (usually 3+).

**Why spread across AZs:**
> 1. **High availability:** If one AZ goes down, other AZs keep your service running (zero downtime)
> 2. **Fault tolerance:** Don't rely on single point of failure
> 3. **Disaster recovery:** Natural disasters, data centre issues only affect one AZ
> 4. **SLA compliance:** Production apps require multi-AZ (most companies mandate it)

---

## 12. Troubleshooting Tools & Commands

### 12.1 Connectivity Testing

| Command            | What It Does                                    | Example                     | What to Look For                              |
| ------------------ | ----------------------------------------------- | --------------------------- | --------------------------------------------- |
| ping               | Tests if host is reachable and measures latency | ping 8.8.8.8                | Response time, packet loss (0% loss = good)   |
| traceroute/tracert | Shows path packets take to destination (hops)   | traceroute google.com       | Where connection breaks, high latency hops    |
| telnet             | Tests if specific port is open/reachable        | telnet example.com 443      | Connected vs connection refused/timeout       |
| nc (netcat)        | Tests port connectivity, can send/receive data  | nc -zv 10.0.1.50 3306       | Open, closed, or timeout (z=scan, v=verbose)  |
| curl               | Tests HTTP/HTTPS connectivity, gets response    | curl -v https://example.com | HTTP status code (200=good, 5xx=server error) |

### 12.2 DNS Troubleshooting

|Command|What It Does|Example|
|---|---|---|
|nslookup|||
|dig|||
|host|||

### 12.3 Network Information

| Command            | What It Shows                                                      | Example              |
| ------------------ | ------------------------------------------------------------------ | -------------------- |
| ip addr / ifconfig | Queries DNS server for IP address of a domain                      | nslookup example.com |
| ip route / route   | Detailed DNS query (shows all record types, authoritative servers) | dig example.com      |
| netstat / ss       | Simple DNS lookup, shows A and MX records                          | host example.com     |

### 12.4 Packet Analysis

**tcpdump basics:**
> tcpdump captures network packets in real-time. Shows source/destination IP, port, protocol, payload snippets.

**When to use packet capture:**
> 1. **Connection timeouts:** Capture traffic to see if packets are reaching destination or getting dropped
> 2. **Application errors:** See what data is actually being sent/received (mismatched payloads, malformed requests)
> 3. **Performance issues:** Identify packet loss, retransmissions, slow responses
> 4. **Security investigation:** Detect suspicious traffic patterns, unauthorised connections
> 5. **Protocol debugging:** Verify correct headers, port usage, handshake completion
> 6. **Network troubleshooting:** Rule out application code (see if network is the problem)

### 12.5 Troubleshooting Methodology

**Step-by-step approach:** 1. 2. 3. 4. 5.

**DevOps Application:**
> Approach:
> 1. **Verify connectivity to destination:** Can you reach the IP/host at all? (ping, traceroute)
> 2. **Confirm DNS resolution:** Does the hostname resolve to correct IP? (dig, nslookup)
> 3. **Test specific port/protocol:** Is the right port open and responding? (telnet, nc, curl)
> 4. **Check network configuration:** Are route tables, security groups, firewalls allowing traffic? (review rules)
> 5. **Capture and analyse packets:** If above passes, see what's actually being sent/received (tcpdump)

**Scenario:** Pod in Kubernetes cluster can't connect to external API at api.example.com:443

**Troubleshooting steps:**
**Step 1: DNS resolution**
```bash
# From inside pod
kubectl exec -it pod-name -- sh
nslookup api.example.com
# Expected: resolves to IP (e.g., 203.0.113.50)
# If fails: DNS issue, check CoreDNS, check /etc/resolv.conf
```

**Step 2: Basic connectivity**
```bash
# From inside pod
ping 203.0.113.50
# Expected: replies with latency
# If timeout: network unreachable, check routing
```

**Step 3: Traceroute to find where path breaks**
```bash
traceroute api.example.com
# Expected: series of hops ending at destination
# If stops midway: routing issue, firewall blocking
```

**Step 4: Test specific port**
```bash
nc -zv api.example.com 443
# Expected: "succeeded"
# If "refused": port closed, API not running
# If "timeout": firewall blocking
```

**Step 5: Full HTTP/HTTPS test**
```bash
curl -v https://api.example.com/health
# Expected: HTTP/1.1 200 OK
# If connection refused: port blocked
# If timeout: firewall, routing, or API down
# If SSL error: certificate issue
```

**If curl succeeds but app fails:**
```bash
# Capture traffic to see what app is actually sending
kubectl exec -it pod-name -- tcpdump -i eth0 -v host api.example.com
# Compare with what curl sent
```

**Common findings and fixes:**

|Finding|Likely Cause|Fix|
|---|---|---|
|nslookup fails|DNS not working|Check CoreDNS pod logs, check /etc/resolv.conf|
|ping timeout|Network unreachable|Check pod network policy, check egress rules|
|traceroute stops at node|Route missing|Check node route table, check CNI plugin|
|nc timeout on port 443|Firewall blocking|Check pod network policy, check node security groups, check API firewall|
|curl succeeds but app fails|App-level issue|Check app logs, check credentials, check request format|
|Packets sent but no response|API down|Check API health, check logs on API server side|

**Example real scenario:**
```bash
# Pod tries to reach payment API, gets timeout
curl https://payment-api.external.com/charge
# timeout after 30s

# Step 1: DNS
nslookup payment-api.external.com
# resolves to 198.51.100.1 ✓

# Step 2: Ping
ping 198.51.100.1
# timeout ✗

# Step 3: Traceroute
traceroute 198.51.100.1
# shows: pod → node → (stops here)

# Likely cause: Node security group blocking outbound traffic
# Fix: Add egress rule to node security group for port 443
```

**DevOps context:** Start simple (DNS, ping), progress to specific (port test), end with packet analysis if needed. 80% of issues caught by step 3. Don't jump to tcpdump first; it's verbose and harder to read. Methodology saves time and isolates problems systematically.

---



## 13. Common DevOps Networking Scenarios

### Scenario 1: Web App Can't Connect to Database

## **Possible causes:**

**How to diagnose:**

> [Your approach]

### Scenario 2: Users Can't Access Website

## **Possible causes:**

**How to diagnose:**
> [Your approach]

### Scenario 3: Intermittent Connectivity Issues

## **Possible causes:**

**How to diagnose:**
> [Your approach]

### Scenario 4: Container Can't Resolve DNS

## **Possible causes:**

**How to diagnose:**
> [Your approach]

### Scenario 5: High Latency Between Services

## **Possible causes:**

**How to diagnose:**
> [Your approach]

---

## Quick Reference Cheat Sheet

### Common Ports
| Port  | Service                        |
| ----- | ------------------------------ |
| 22    | SSH (secure remote access)     |
| 53    | DNS (domain name resolution)   |
| 80    | HTTP (unencrypted web traffic) |
| 443   | HTTPS (encrypted web traffic)  |
| 3306  | MySQL (database)               |
| 5432  | PostgreSQL (database)          |
| 6379  | Redis (cache)                  |
| 27017 | MongoDB (NoSQL database)       |
### CIDR Quick Reference
| CIDR | Hosts      | Subnet Mask     |
| ---- | ---------- | --------------- |
| /8   | 16,777,214 | 255.0.0.0       |
| /16  | 65,534     | 255.255.0.0     |
| /24  | 254        | 255.255.255.0   |
| /28  | 14         | 255.255.255.240 |
| /32  | 1          | 255.255.255.255 |
### Private IP Ranges
|Class|Range|
|---|---|
|A|10.0.0.0 to 10.255.255.255 (10.0.0.0/8)|
|B|172.16.0.0 to 172.31.255.255 (172.16.0.0/12)|
|C|192.168.0.0 to 192.168.255.255 (192.168.0.0/16)|

---

_Last updated: [26/02/26]_