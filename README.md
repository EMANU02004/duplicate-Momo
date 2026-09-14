# MoMo SMS Analytics

**Team:** Brain Boosters

## Project Description

An enterprise-level fullstack application that processes MTN Mobile Money (MoMo) SMS transaction data
provided as XML. The pipeline parses, cleans, and categorizes the raw SMS records, loads them into a
relational (SQLite) database, and exposes the results through a frontend dashboard for analysis.

## Team Members

- Emmanuel Masambu — [EMANU02004](https://github.com/EMANU02004)
- Pauline — [pmiyienda-dotcom](https://github.com/pmiyienda-dotcom)
- Marion Gitau — [mgitau-sys](https://github.com/mgitau-sys)

Here is the 🔗 [System Architecture Diagram](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&target=blank&highlight=0000ff&edit=_blank&layers=1&nav=1&title=System%20architecture&dark=auto#R%3Cmxfile%3E%3Cdiagram%20name%3D%22Page-1%22%20id%3D%22_tWC84w68V833Dc4xFwV%22%3E7Vpbc6IwGP01zuw%2BtCMgqI%2FWy7YzOnVrd7p96gSIkDYSN4Sq%2B%2Bs3kQQEtGsdsdLpS8t3cuWc8yUxWjO6s%2BUPCub%2BiLgQ1%2FS6u6wZvZqut406%2FyuAVQyYzWYMeBS5MaSlwAT9hRKU7bwIuTDMVGSEYIbmWdAhQQAdlsEApWSRrTYlODvqHHiwAEwcgIvoA3KZH6Mts57i1xB5vhpZq8uSGVCVJRD6wCWLDcjo14wuJYTFT7NlF2LBneIlbjfYUZpMjMKA7dPgaUhw9HDXvHhi%2BPHlobvsDGYXmuwGugUa0n4lFJKIOvCtzmQ9tlLsiW4nMgxIwP9dORF9hWJKGg8oiQJ3HdV5RCjziUcCgIeEzGWVZ8jYSvoCRIxwyGczLEunJGCyUOOMXoUMUAW0eAwDdyOS%2FgHUg%2ByN97Dieq8AR%2FI9Erm4zSGZQUZXvAKFGDD0miUOSMN5Sb1UE%2F4gZXmPRLsFSYlOiRSsLHzE4GQO1moteF5mSdv6ehyAlMHlxgjFN%2FY3rG5JXy%2FStNCV%2BWUvhvK%2BTH5NxccnqXFEH%2Bun9zGfI139lu3XwaMILk0V9pabhb2VjErxf%2BMj7a5Xx%2B6JnVUvrazd9UZpdjeOaHfj3JftJDm09yXHiewum44J4swnZrC0rBmMds4M8bxkq5wfkmkcbhGjQnnUyOaRaZ4qjxoVIim32BiWmfWXVdpiUz%2FiYmOe%2B2Kz56KhbRX6ozZN8%2FP4WCvLxq0jutj6JC42zsrF7S%2BFdh2Hz0QhTf%2BSaNch4kwksvbZCkIfzMWjs8KIM0qN%2F28Idsz90E4A4Lx4a0VuI8a7gRIPJb%2Fm0XaRVnEXaec2kfwnL6O0w9Be%2FPK3Y1n6trEbMkpeYJdgQlPDTxHGOQhg5AVCLT4i5PiV4A85AHdkwQy5rhg6lyAF9ke3o1uOTEaTyu%2FmWrPCOvQAA2LulDgwDFHg1XQLi4nalD954ukbJsANvx9Np%2FzNXF6n8m7mWhUWagBC1hnfhFv0YRQEIXAYIgEvHgC%2BDa34GOVJZjZPdrvUrrBkLgh9mwDqXj6HJNgiHPA8Cj3AYHlSae1TSaXStpJSTX4Ot%2BgjFkcbhPAwdRrvPyuUdnGijjuVFKen8miLRAto88q2%2BHYV0uNl0YfdcOl73QPuJxThREzx%2Boten1MNgwLVBYkK3CvKxceVzBysPxFRBRfxQbvDK%2Bj6fLnuR5UrpVRHKA%2FYCpBHws54LA6Gj5P7%2FkiEd93rm%2Ft%2B9%2F7XXV814cza%2BW44VuiaY%2FG8FXyAOxIrbNgjkV92o%2Bcu2BsHLLI8TL%2BAj2%2Fe018xGP1%2F%3C%2Fdiagram%3E%3C%2Fmxfile%3E)

## Scrum Board

We use Trello to organize our tasks and track their progress throughout the project.

[View our Trello Scrum Board](https://trello.com/invite/b/6a9a920f7b041f8dee0b5906/ATTI877c1395fc0e4fb750c4442870a355503703FA59/momo-app)



| Layer | Technology | Location |
|---|---|---|
| Raw Data | XML / JSON | `data/raw/`, `dsa/` |
| ETL Pipeline | Python | `etl/` |
| Database | SQLite (runtime) / MySQL (design) | `data/db.sqlite3`, `database/` |
| API | FastAPI | `api/` |
| Frontend | HTML / JS / CSS | `index.html`, `web/` |
| Tests | pytest | `tests/` |

## Database Design (Week 2)

### ERD & Design Rationale
See [`docs/erd_design.md`](docs/erd_design.md) for the full ERD specification and design rationale, and `docs/erd_diagram.png` for the Draw.io export.

### Tables

#### `transaction_categories`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT UNSIGNED | PK AUTO_INCREMENT | Surrogate key |
| `name` | VARCHAR(50) | UNIQUE, CHECK (7 values) | Category slug |
| `description` | VARCHAR(255) | | Human-readable label |
| `created_at` | DATETIME | DEFAULT NOW | Row creation time |

#### `users`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT UNSIGNED | PK AUTO_INCREMENT | Surrogate key |
| `phone` | VARCHAR(20) | UNIQUE, CHECK E.164 | Phone number |
| `display_name` | VARCHAR(100) | | Name parsed from SMS |
| `created_at` | DATETIME | DEFAULT NOW | Row creation time |

#### `transactions`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT UNSIGNED | PK AUTO_INCREMENT | Surrogate key |
| `user_id` | INT UNSIGNED | FK → users | Account owner |
| `category_id` | INT UNSIGNED | FK → transaction_categories | SMS category |
| `address` | VARCHAR(20) | | Raw sender address |
| `date` | DATETIME | | Transaction timestamp (UTC) |
| `body` | TEXT | | Original SMS text |
| `amount` | DECIMAL(15,2) | NULLABLE, ≥ 0 | Extracted RWF amount |
| `body_hash` | CHAR(64) | UNIQUE | SHA-256 for deduplication |
| `created_at` | DATETIME | DEFAULT NOW | Row creation time |

#### `transaction_parties` *(junction — resolves M:N)*
| Column | Type | Constraints | Description |
|---|---|---|---|
| `transaction_id` | INT UNSIGNED | PK, FK → transactions | |
| `user_id` | INT UNSIGNED | PK, FK → users | |
| `role` | VARCHAR(20) | PK, CHECK (4 values) | sender / receiver / agent / merchant |

#### `system_logs`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT UNSIGNED | PK AUTO_INCREMENT | Surrogate key |
| `transaction_id` | INT UNSIGNED | NULLABLE FK → transactions | NULL for pipeline-level events |
| `level` | VARCHAR(10) | CHECK (INFO/WARNING/ERROR) | Log severity |
| `event` | VARCHAR(100) | | Short event code |
| `message` | TEXT | | Detailed message |
| `created_at` | DATETIME | DEFAULT NOW | Log timestamp |

### Key Relationships
- `users` → `transactions` : **1 : M** (one owner, many transactions)
- `transaction_categories` → `transactions` : **1 : M**
- `transactions` ↔ `users` via `transaction_parties` : **M : N** (junction table)
- `transactions` → `system_logs` : **1 : M**

### Deliverable Files
| File | Purpose |
|---|---|
| `database/database_setup.sql` | Full DDL + sample DML + CRUD queries |
| `examples/json_schemas.json` | JSON schemas for all entities + complex nested example |
| `docs/erd_design.md` | ERD spec, cardinality table, design rationale |
| `docs/momo_ERD.png` | Draw.io ERD export |

## Project Structure
```
.
├── README.md
├── .env.example
├── requirements.txt
├── index.html
├── docs/                          ← Week 2: ERD & design docs
│   ├── erd_design.md
│   └── erd_diagram.png
├── database/                      ← Week 2: MySQL setup script
│   └── database_setup.sql
├── examples/                      ← Week 2: JSON schemas
│   └── json_schemas.json
├── web/
│   ├── styles.css
│   ├── chart_handler.js
│   └── assets/
├── data/
│   ├── raw/
│   │   └── momo.xml
│   ├── processed/
│   │   └── dashboard.json
│   ├── logs/
│   │   └── dead_letter/
│   └── db.sqlite3
├── etl/
│   ├── __init__.py
│   ├── config.py
│   ├── parse_xml.py
│   ├── clean_normalize.py
│   ├── categorize.py
│   ├── load_db.py
│   └── run.py
├── api/
│   ├── __init__.py
│   ├── app.py
│   ├── db.py
│   └── schemas.py
├── scripts/
│   ├── run_etl.sh
│   ├── export_json.sh
│   └── serve_frontend.sh
├── tests/
│   ├── test_parse_xml.py
│   ├── test_clean_normalize.py
│   ├── test_categorize.py
│   ├── test_load_db.py
│   └── test_api.py
└── dsa/
    ├── sms_data.json
    ├── schema.json
    ├── categories.json
    └── sample_output.json
```
