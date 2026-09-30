# Server Health Check Commands

| Resource | Command | Reports | Units |
|---|---|---|---|
| CPU | `nproc` | Number of logical CPU cores | count |
| CPU | `lscpu` | Model, cores, threads, base/max MHz, cache | text/MHz |
| CPU | `uptime` | Load average (1/5/15 min) | avg running processes |
| CPU | `top -bn1 \| head -20` | Live per-process CPU% snapshot | % |
| CPU | `mpstat 1 3` *(needs `sysstat`)* | Per-core CPU utilization over 3×1s samples | % |
| RAM | `free -h` | Total / used / free / available / swap | GiB/MiB |
| RAM | `cat /proc/meminfo` | Full memory breakdown (MemTotal, Buffers, Cached, SwapFree, etc.) | kB |
| RAM | `vmstat 1 5` | Memory + swap activity, 5×1s samples | KB, plus si/so swap rate |
| Disk | `df -h` | Per-filesystem used/available/total | GB/GiB |
| Disk | `du -sh /path/*` | Size of each item in a directory | GB/MB |
| Disk | `lsblk` | Block devices, partitions, mount points | GB |
| Disk | `iostat -dx 1 3` *(needs `sysstat`)* | Disk read/write throughput, IOPS, %util | KB/s, IOPS, % |
| Disk | `smartctl -a /dev/sda` *(needs `smartmontools`)* | Drive health, reallocated sectors, temp | pass/fail + raw values |
| Network | `ip -s link` | Per-interface RX/TX bytes, errors, drops | bytes/packets |
| Network | `ss -tulpn` | Listening ports + owning process | port/proto |
| Network | `curl -s ifconfig.me` | Public IP | IP address |
| Docker | `docker stats --no-stream` | Per-container CPU%, MEM used/limit, NET I/O, BLOCK I/O | %, MiB/GiB |
| Docker | `docker system df` | Disk used by images/containers/volumes/build cache | GB |
| Docker | `docker ps -a` | Container status, uptime, restart count | text |
| Temperature | `sensors` *(needs `lm-sensors`)* | CPU/chipset temps, fan speeds | °C, RPM |

## Takeaways

### 1. The top 3 most important commands
If you only run three, run these — they cover the three ways a self-hosted stack actually dies:
- `free -h` — RAM exhaustion is the single most common cause of a Docker host silently killing containers (OOM killer), and it gives zero warning in logs unless you know to look.
- `df -h` — a full disk doesn't degrade gracefully; Postgres and n8n both fail hard (writes rejected, workflows stop executing) the moment their volume hits 100%.
- `docker stats --no-stream` — the only one of these that tells you *which container* is the problem, not just that the host is under load. Without it, `free -h`/`top` tell you something's wrong but not what to restart.

### 2. How to detect critical issues with these
Thresholds that actually mean something, not just "the number is high":
- **RAM**: in `free -h`, watch `available`, not `free`. Linux caches aggressively, so `free` looks low even when healthy — `available` is the real number. If `available` is under ~10% of total, or `swap used` is climbing and not going back down, you're close to OOM kills.
- **Disk**: in `df -h`, 80% used is your action threshold, not 100% — Postgres and Docker both need headroom for WAL logs, temp files, and image layers during updates. Hitting 100% mid-write is how databases corrupt.
- **CPU**: in `uptime`, a load average sustained above your core count (`nproc`) means things are queuing, not just busy. A single spike is fine; a load average that stays above `nproc` across the 5- and 15-minute numbers is the actual signal.
- **Docker**: in `docker stats`, a container pinned near its MEM limit with climbing usage is about to get OOM-killed by Docker itself — check `docker ps -a` afterward for an `Exited (137)` status, which is Docker's signature for exactly that.

### 3. Super takeaways — the non-obvious ones
- **A healthy-looking average hides a dying container.** Host-level `free -h`/`top` numbers can look completely fine while one specific container (say, a runaway n8n execution or an Ollama model stuck reloading) is the one about to crash. `docker stats` per-container is not optional if you're running a multi-service stack — host-level checks alone will miss it.
- **Correlate, don't check in isolation.** Rising disk I/O (`iostat`) plus climbing swap (`vmstat`) together usually means you've run out of RAM and the kernel is swapping to disk — which then *also* tanks disk performance for everything else (Postgres included). Seeing one of these alone is noise; seeing both together is the real incident.
- **This table is a manual version of what Uptime Kuma should be doing for you.** You already planned to install it — the actual endgame here isn't memorizing these commands, it's wiring a heartbeat/health check into Uptime Kuma so you get paged before you'd have thought to run any of these by hand. Treat this file as the spec for what to monitor, not a permanent daily routine.
