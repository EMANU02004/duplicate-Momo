# ERD Design — MoMo SMS Analytics
**Team:** Brain Boosters

---

## Entity Relationship Diagram

> The diagram file `erd_diagram.png` (exported from Draw.io) is located in this `/docs` folder.

### Entities & Relationships at a Glance

```
transaction_categories (1) ──────< (M) transactions (M) >────── (1) users
                                          │
                                          │ (1)
                                          │
                                          ▼ (M)
                                  transaction_parties (M) >────── (1) users
                                          │
                                  (junction — resolves M:N)

transactions (1) ──────< (M) system_logs
```

### Entities

| Entity | PK | Description |
|---|---|---|
| `transaction_categories` | `id` | 7-value lookup for SMS category |
| `users` | `id` | Any phone number party (owner, sender, receiver, agent, merchant) |
| `transactions` | `id` | One row per unique SMS; FK to `users` (owner) and `transaction_categories` |
| `transaction_parties` | `(transaction_id, user_id, role)` | **Junction table** — resolves M:N between `transactions` and `users` |
| `system_logs` | `id` | ETL audit trail; optionally linked to a `transaction` |

### Cardinalities

| Relationship | Type | Explanation |
|---|---|---|
| `users` → `transactions` | 1 : M | One account owner has many transactions |
| `transaction_categories` → `transactions` | 1 : M | One category classifies many transactions |
| `transactions` ↔ `users` (via `transaction_parties`) | **M : N** | A transaction involves multiple parties; a user appears in many transactions |
| `transactions` → `system_logs` | 1 : M | One transaction can generate multiple log entries |

---

## Design Rationale (≈ 270 words)

The schema is built around the single source of truth in the MoMo data: the **SMS message itself**. Every design decision flows from that anchor.

**`transactions` as the fact table.** Each SMS is unique (enforced by `body_hash UNIQUE`), carries a timestamp, an amount, and belongs to exactly one category. Storing the raw `body` alongside the extracted `amount` preserves the original evidence for auditing and re-processing without re-parsing the XML.

**Separating `transaction_categories` into a lookup table** rather than a plain `TEXT` column achieves two things: it enforces the closed set of seven valid categories at the database level (via `FOREIGN KEY` + `CHECK`), and it makes category-level aggregations cheaper because the engine joins on an integer rather than comparing variable-length strings.

**`users` as a phone-number registry.** The XML data identifies parties only by phone number. Normalising these into a `users` table eliminates redundant storage, enables name enrichment over time (the `display_name` column starts empty and is filled as names are parsed from SMS bodies), and provides a single place to enforce the E.164 format constraint.

**`transaction_parties` resolves the M:N relationship.** A single transaction can involve up to four distinct roles (sender, receiver, agent, merchant). Encoding this as a junction table with a `role` column is far more flexible than adding four nullable FK columns to `transactions`, and it correctly models the many-to-many reality: one user can be a party in thousands of transactions, and one transaction can have multiple parties.

**`system_logs` for observability.** The ETL pipeline needs a durable audit trail. Linking logs optionally to a `transaction_id` (nullable FK with `ON DELETE SET NULL`) means pipeline-level events (start, finish) and record-level warnings (missing amount, duplicate) coexist in one table without requiring two separate log tables.

**Indexes** are placed on every FK column and on `date` and `amount` — the two columns most likely to appear in `WHERE` and `ORDER BY` clauses in the analytics API.
