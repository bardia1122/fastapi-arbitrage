# 💱 Cloud Computing Homework 01 – Arbitrage Service

**Developed by:** Bardia Sabbagh Kermani  
**Course:** Cloud Computing – Homework 01  
**Instructor:** Dr. Ahmad Javadi

---

A **FastAPI-based cloud service** that discovers **crypto arbitrage opportunities** between Iranian exchanges **Wallex** and **Nobitex**, stores price snapshots in a PostgreSQL database, and sends **real-time alerts via Telegram and Bale bots**.  
The project also exposes **Prometheus metrics** and provides a **Grafana dashboard** for monitoring.

---

## 🧩 Project Overview

This project was built as part of the **Cloud Computing Course** to demonstrate skills in:
- Cloud-based service deployment  
- Asynchronous data collection  
- API integration  
- Database persistence  
- Real-time alerting  
- Service monitoring with Prometheus & Grafana

The service periodically compares crypto prices between **Wallex** and **Nobitex** to detect profitable arbitrage opportunities and notifies users via Telegram and Bale.

---

## 🏗️ Project Structure

```
.
│   .env
│   docker-compose.yml
│   Dockerfile
│   requirements.txt
│
├───app
│   │   main.py                # FastAPI entrypoint
│   │   settings.py            # Environment configuration
│   │
│   ├───api
│   │       routes.py          # API routes (health, metrics, opportunities)
│   │
│   ├───core
│   │       arbitrage.py       # Arbitrage detection logic
│   │       scheduler.py       # Background scanning loop
│   │       telegram.py        # Telegram notification sender
│   │       bale.py            # Bale notification sender
│   │       metrics.py         # Prometheus metric definitions
│   │
│   ├───db
│   │       models.py          # SQLAlchemy ORM models
│   │       crud.py            # Database operations
│   │       session.py         # Async session management
│   │
│   ├───exchanges
│   │       nobitex.py         # Nobitex API integration
│   │       wallex.py          # Wallex API integration
│   │       symbols.py         # Symbol normalization helpers
│   │       types.py           # Exchange ticker typing
│   │
│   └───schemas
│           arbitrage.py       # Pydantic output models
│
├───ops
│   ├───grafana
│   │   └───provisioning
│   │       ├───dashboards
│   │       │       fastapi-arb.json
│   │       └───datasources
│   │               datasource.yml
│   └───prometheus
│           prometheus.yml
│
└───tests
```

---

## ⚙️ Core Components

### 🔹 FastAPI Service
- **Entrypoint:** `app/main.py`
- **Routes:**
  - `GET /health` – Service health check
  - `GET /metrics` – Prometheus metrics endpoint
  - `GET /opportunities` – Retrieve recent arbitrage detections
  - `POST /arbitrage/scan` – Manual trigger for arbitrage scan
  - `GET /prices` – Retrieve latest stored prices

### 🔹 Arbitrage Engine
- Collects market data from **Wallex** and **Nobitex**
- Normalizes prices and computes percentage difference
- Stores prices and opportunities in PostgreSQL
- Sends notifications when profit exceeds configured threshold

### 🔹 Notification System
- **Telegram Bot:** via `telegram.py`
- **Bale Bot:** via `bale.py`
- Each alert includes:
  - Pair symbol  
  - Buy/Sell exchanges  
  - Prices and percentage difference  
  - Timestamp

### 🔹 Database
- **PostgreSQL (async via SQLAlchemy 2.0 + asyncpg)**
- Tables:
  - `price_snapshots`
  - `opportunities`
- Connection configured via `.env` → `DATABASE_URL`

### 🔹 Monitoring
- Prometheus scrapes the `/metrics` endpoint.
- Grafana visualizes the service and database metrics using the included JSON dashboard.

---

## 🚀 Deployment (Docker Compose)

The project is fully containerized and runs as a multi-service stack.

### 1️⃣ Clone Repository
```bash
git clone https://github.com/bardia1122/fastapi-arbitrage.git
cd cloud-arbitrage-service
```

### 2️⃣ Configure Environment
Create a `.env` file:
```bash
APP_NAME=Arbitrage Service
API_PREFIX=/api
HOST=0.0.0.0
PORT=8000
DEBUG=True

DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/arbitrage

SYMBOLS=[USDT-IRT,BTC-USDT]
SCAN_INTERVAL_SEC=7
PROFIT_PCT_THRESHOLD=0.5

TELEGRAM_BOT_TOKEN=<your_bot_token>
TELEGRAM_CHAT_ID=<your_chat_id>
BALE_BOT_TOKEN=<your_bale_token>
BALE_CHAT_ID=<your_bale_chat_id>
NOTIFY_CHANNEL=<your_preferred_bot> (telegram or bale)
```

### 3️⃣ Launch Containers
```bash
docker-compose up --build
```

### 4️⃣ Access Services

| Service | URL |
|----------|-----|
| FastAPI Docs | http://localhost:8000/docs |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
| Metrics | http://localhost:8000/metrics |

---

## 📊 Prometheus Metrics

| Metric | Description |
|--------|--------------|
| `exchange_response_time_seconds` | Exchange API response latency |
| `exchange_requests_total` | Number of exchange requests by status |
| `arbitrage_events_total` | Total arbitrage events detected |
| `arbitrage_last_diff_percent` | Latest percentage difference per pair |
| `arbitrage_last_diff_value` | Latest absolute difference per pair |

---

## 📈 Grafana Dashboard

**Dashboard file:** `ops/grafana/provisioning/dashboards/fastapi-arb.json`

**Panels include:**
- ⏱ Exchange response time (s)
- 📊 Requests per exchange (ok/error)
- 💰 Last diff percent per symbol
- 💰 Last diff value per symbol
- 💾 Database size
- ⚙️ Transaction rates (commits / rollbacks)
- 🟢 Database up status
- 📈 Active DB connections
- 🪙 Arbitrage discovery rate (per 5-minute window)

---

## 🧪 Example Telegram/Bale Alert

```
Arbitrage
• Symbol: BTC-USDT
• Buy @nobitex: 107,123.45
• Sell @wallex: 107,650.00
• Diff: 526.55 (0.49%)
```

---

## 🧠 Technologies Used

| Category | Stack |
|-----------|-------|
| Backend Framework | FastAPI |
| Async HTTP | aiohttp |
| ORM / DB Layer | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL |
| Monitoring | Prometheus + Grafana |
| Containerization | Docker, Docker Compose |
| Messaging | Telegram & Bale Bots |
| Language | Python 3.10+ |

---

## 🧾 Acknowledgements

- [Nobitex API Docs](https://apidocs.nobitex.ir/?shell)  
- [Wallex API Docs](https://developers.wallex.ir/basicservices/latesttrades)  
- [Prometheus Documentation](https://prometheus.io/docs/)  
- [Grafana Documentation](https://grafana.com/docs/)

---

## 📜 License

This project was developed for **educational purposes** as part of the *Cloud Computing Course, 2025*.  
© 2025 **Bardia Sabbagh Kermani**. All rights reserved.

---
