# CoinFlow — Personal Finance Tracking Telegram Bot

![Python](https://img.shields.io/badge/Python-3-blue)
![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

---

## Project Overview

CoinFlow is a Telegram bot for tracking personal income and expenses through plain text messages, with PIN-based access control, monthly/overall statistics, and full transaction history.

A user simply sends a message like `-250 coffee` or `+5000 salary bonus` and the bot parses the operation type, amount, category, and comment automatically, creating new categories on the fly when needed.

---

## Motivation

This was my first Telegram bot project, built for personal use — I'd rather rely on something I can extend or rework myself than depend on someone else's app.

---

# Features

## Access Control

- Shared PIN-code authorization
- Permanent authorization per Telegram user (no re-entry required)
- Custom filter gating every other command behind authorization
- Fallback handler for unrecognized or unauthorized messages

## Expense & Income Tracking

- Single-line text parsing (`-250 coffee` / `+5000 salary note`)
- Automatic category creation on first use
- Category name normalization (capitalization) to prevent duplicate categories from inconsistent casing
- Confirmation message showing the last 10 transactions after every entry

## Statistics & History

- `/stats` — aggregated totals for a chosen month or all-time, split into income and expenses, with each category's share shown as a percentage of the total
- `/history` — full list of individual transactions for a chosen period, with date, category, amount, and comment
- Timezone-aware timestamps: stored in UTC, displayed converted to the local timezone

## Infrastructure

- Docker & Docker Compose
- SQLite database persisted via a mounted volume, surviving container rebuilds
- Custom Telegram command menu (`set_my_commands`)

---

# Technical Challenges

## FSM-Based Authorization Flow

Telegram messages are stateless by default — the bot has no inherent way to know that a user's next message is meant to be a PIN code rather than a transaction or a random message.

This is solved using aiogram's Finite State Machine: after `/login`, the user is moved into a `waiting_for_pin` state, and a dedicated handler — filtered specifically on that state — captures the next message and validates it against the configured PIN. On success, the user's Telegram ID is stored permanently; on failure, the state is preserved so the user can retry without restarting the flow.

The same state-based pattern is reused for period selection in `/stats` and `/history`, keeping multi-step conversations consistent across the bot.

## Repository Pattern for Data Access

Rather than calling SQLAlchemy directly from the service layer, each entity (`Category`, `Transaction`, `AuthorizedUser`) is wrapped in a dedicated repository class exposing narrow, purpose-built methods (`get_by_name`, `get_by_month`, `exists`, etc.).

This keeps the service layer free of query details and makes each entity's data-access contract explicit in one place, rather than scattered across handlers.

## Category Consistency

Because categories are created implicitly from free-text user input, the same category could easily end up duplicated under different casing (`coffee` vs `Coffee` vs `COFFEE`), silently splitting statistics across multiple rows.

Category names are normalized (capitalized) *before* the lookup-or-create step runs, so that both the search and the creation path always operate on the same canonical form, guaranteeing one category per name regardless of how the user typed it.

## SQLite Persistence in Docker

Since the container's filesystem is ephemeral, the database file is stored outside the container in a mounted volume rather than being baked into the image. This means the bot's image can be rebuilt freely — after adding a new feature, for example — without ever risking the underlying transaction history.

---

# Technology Stack

### Bot Framework
- Python
- aiogram 3

### Database
- SQLite
- SQLAlchemy

### Architecture
- Repository pattern
- Service layer

### Infrastructure
- Docker
- Docker Compose

---

# Project Structure

```text

finance_bot/
├── bot/               # Bot & Dispatcher setup, router registration
├── handlers/           # Command & state handlers (auth, expenses, stats, history)
├── filters/             # Custom filters (e.g. IsAuthorized)
├── services/              # Business logic (parsing, aggregation, timezone conversion)
├── repositories/            # Data access layer, one repository per entity
├── models/                    # SQLAlchemy models
├── db/                          # Engine & session setup
├── config.py
├── main.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt

```

---

# Environment Variables

Create a `.env` file inside the project directory.

| Variable | Description |
|-----------|-------------|
| BOT_TOKEN | Telegram bot token from @BotFather |
| PIN_CODE | Shared PIN code required for authorization |

---

# Running the Project

```bash
git clone https://github.com/Ophion666/TelegramBot-CoinFlow.git
docker compose up --build -d
```

The database file is persisted in the `data/` directory on the host machine, so it survives container restarts and rebuilds.

---

# Future Improvements

- Per-category budgets with limit warnings
- Inline keyboards for period selection instead of free-text input
- Export history to CSV

---

# Technical Experience

This project gave me practical experience with:

- building an event-driven bot with aiogram and asyncio
- designing multi-step conversational flows with a Finite State Machine
- applying the Repository pattern outside of a typical REST API context
- handling timezone-aware datetimes correctly across storage and display
- persisting a file-based database safely inside a containerized environment
