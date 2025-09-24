
# Simple Proxy Scraper & Checker

This project provides a minimal Python script (`nig.py`) that:
- Scrapes public raw proxy lists (HTTP) from a few GitHub sources.
- Collects unique host:port style proxies.
- Checks each proxy by making a test request to `https://httpbin.org/ip` using the proxy.
- Prints a final list of proxies that responded successfully.

> Educational / testing use only. Many free proxies are unreliable or unsafe. Do **not** use untrusted proxies for sensitive traffic.

---
## Contents
- `nig.py` – main script with two tiny classes:
  - `AK.scrape(urls)` – fetch & parse proxies line-by-line.
  - `Ahmd.check(proxy)` – test a single proxy.
  - `run()` – orchestrates scrape + threaded checks.

---
## Quick Start
### Requirements
Python 3.8+ and the `requests` library.

Install dependency (if needed):
```bash
pip install requests
```

### Run
```bash
python nig.py
```
You should see output like:
```
Good proxies: ['123.45.67.89:8080', '...']
```
(Usually many will fail; that's normal for public lists.)

---
## How It Works
1. A list of raw proxy source URLs (plain text) is defined in `run()`.
2. `AK.scrape` downloads each one with `requests.get` (8 second timeout), splits lines, keeps those that look like `host:port`.
3. Each candidate proxy is tested in a separate thread calling `Ahmd.check` (6 second timeout) against `https://httpbin.org/ip`.
4. Working proxies are appended to a shared list protected by a lock.
5. Final list printed.

---
## Known Issues / To Improve
The current file (as checked in) has some structural issues you may want to fix before heavy use:
- Indentation errors around the `try:` block in `AK.scrape` (Python will raise a syntax error as written).
- Thread list (`threads`) is referenced but never initialized inside `run()`; creation of threads is missing.
- A stray import `from asyncio import threads` is unnecessary.
- No rate limiting or max thread cap (could create too many threads for large proxy sets).
- No user-agent header; some sources may block default Python requests.
- No persistence (results only printed, not saved).

### Suggested Fixes (Minimal Patch Concept)
Inside `run()` you likely intended something like:
```python
threads = []
for p in all_proxies:
    t = threading.Thread(target=worker, args=(p,), daemon=True)
    t.start()
    threads.append(t)
```
And ensure the `try:` inside `AK.scrape` wraps the request logic properly.

---
## Customization
- Add or remove proxy source URLs in the `sources` list inside `run()`.
- Change timeouts by adjusting `timeout=` values in `requests.get` calls.
- Save good proxies:
```python
# after building 'good'
with open('good_proxies.txt', 'w') as f:
    f.write('\n'.join(good))
```
- Filter for HTTPS only by adding a secondary verification endpoint.

---
## Safety & Ethics
- Public proxies can inject, log, or tamper with traffic.
- Never send credentials, tokens, or personal data through untrusted proxies.
- Respect source bandwidth; avoid aggressive re-scraping.

---
## Ideas for Next Steps
| Enhancement | Benefit |
|-------------|---------|
| Limit concurrent threads (Semaphore) | Prevent resource spikes |
| Retry logic (1–2 retries) | Salvage transient network errors |
| Latency measurement | Rank proxies by speed |
| Concurrent scraping (threads for sources) | Faster startup |
| Output JSON/CSV | Machine-readable export |
| Add CLI flags (argparse) | Flexible usage |

---
## Attribution / License
You are free to modify and redistribute. Add an explicit license file (e.g., MIT) if you plan to share publicly.

---
## Disclaimer
This is a simplistic educational tool. Reliability of free proxies is low; use at your own risk.
