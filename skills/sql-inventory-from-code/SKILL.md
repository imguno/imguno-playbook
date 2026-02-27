---
name: sql-inventory-from-code
description: Collects and maintains a complete CSV-based SQL query inventory (SSOT) by extracting all SQL statements from a service application's source code. This skill's only deliverable is the inventory CSV. Use when extracting SQL from application source code, building a query inventory from the codebase, or preparing for SQL tuning from code.
---

# SQL Inventory from Code

This skill defines how to build and maintain a **complete SQL inventory** by extracting SQL statements from a service application's **source code**.

The goal is to:

* Find all SQL used in the application codebase
* Centralize them into a structured CSV file
* Make them traceable and future-proof

**This skill's only deliverable is the inventory CSV.** No index design, no query rewriting, no runtime capture.

This skill is **code-only**. It does not cover DB logs, APM, or runtime query capture. (DB logs and APM are out of scope; they may be used elsewhere for coverage verification but are not part of this skill.)

---

# Core Principle

All SQL present in the application code must be registered in a single structured file:

```
templates/sql_catalog.csv
```

This inventory acts as the **Single Source of Truth (SSOT)** for:

* Query visibility
* Filtering/sorting/pagination pattern analysis
* Preparing future tuning work

---

# What Counts as “SQL in Code”

Include SQL found in:

* Raw SQL strings (inline strings)
* Repository / DAO layers
* Query builder outputs (where the final SQL template exists in code)
* Named queries / XML mappings
* Stored procedure invocations (e.g., `CALL proc_name(...)`)
* Migration/seed scripts **only if** they run as part of the service runtime (otherwise mark as non-runtime)

Exclude (unless explicitly required):

* One-off admin scripts not deployed with the service
* Ad-hoc local/debug queries

---

# How to Discover All Queries (Code Strategy)

## 1. Search Raw SQL Patterns

Search for common tokens:

* `SELECT`, `INSERT`, `UPDATE`, `DELETE`
* `FROM`, `JOIN`, `WHERE`, `ORDER BY`, `GROUP BY`

Recommended actions:

* Grep/ripgrep for SQL keywords
* Scan constant files where SQL templates are stored
* Scan repository/mapper directories

Note:

* If SQL is split across concatenated strings, reconstruct it into a canonical single statement for the inventory.

---

## 2. Identify ORM / Query Builder SQL Templates

Some frameworks generate SQL at runtime but still define templates/structures in code.

Capture:

* Named query definitions
* Mapper XML/DSL definitions
* Query builder fragments when the final structure is deterministic

If a query is truly dynamic (structure changes based on runtime conditions), register:

* The canonical base query
* Each meaningful structural variant (separate rows)

---

## 3. Normalize and Deduplicate

Many queries differ only by parameter values or whitespace.

Normalize by:

* Replacing literal values with placeholders
* Standardizing whitespace
* Converting into parameterized form (`?`, `:name`, `$1`, etc.)

Each structurally identical query should be registered once.

---

# Inventory Rules

## 1. One Query Structure = One Row

Each distinct SQL structure must have one row.

If the same query is used in multiple modules/endpoints, keep a single row and record the primary usage.

---

## 2. Stable Query ID

* Each query must have a unique `query_id`.
* The `query_id` must never change.
* Historical entries must not be deleted.

---

## 3. Required Metadata

Each row must include structured metadata:

* **Location (for traceability):** `file_path`, `function_or_method`, `line_range`
* **Context:** `execution_context` (e.g. `api`, `batch`, `worker`, `cron`, `admin`)
* **Query structure:** `main_table`, `joined_tables`, `where_columns`, `order_by_columns`, `pagination_type`, `has_or_condition`, `has_like`, `like_pattern_type`, `uses_function_on_column`, `full_scan_risk`
* **Optional:** `sql_dialect` or `db_engine` (e.g. MySQL, Postgres, SQLite) when relevant for downstream use

The purpose is to avoid repeatedly parsing raw SQL and to make each entry traceable back to code.

---

# Inventory Creation Workflow

## Step 1 — Collect

* Extract SQL from the application codebase
* Reconstruct concatenated SQL where needed
* List all structural variants for dynamic queries

## Step 2 — Normalize

* Remove literal values
* Convert to parameterized format
* Standardize formatting
* When SQL in code uses string placeholders or interpolated values (e.g. `:id`, `?`, `$1`, template vars), infer they are bound parameters and normalize to one canonical form per structure.

## Step 3 — Register in CSV

For each unique SQL structure:

* Assign `query_id`
* Fill metadata consistently
* Escape SQL correctly

## Step 4 — Validate (Code Coverage)

Before committing:

* Ensure all repository/DAO/mapper locations were scanned
* Ensure the most important endpoints/jobs are represented
* Ensure dynamic query variants are included when they change structure

---

# Metadata Interpretation Guidelines

## Code Location (file_path, function_or_method, line_range)

* `file_path`: Repository-relative path (e.g. `src/repository/UserRepository.java`)
* `function_or_method`: Method or function name where the SQL is defined or invoked
* `line_range`: Optional; e.g. `120-125` or single line `120`

Fill these when the SQL is extracted from code so the inventory remains traceable.

## Execution Context

* `api` → HTTP/gRPC API handler
* `batch` → batch job
* `worker` → background worker / queue consumer
* `cron` → scheduled job
* `admin` → admin-only or internal tool

## WHERE Columns

* List only column names
* No operators
* Comma-separated format

Example:

```
"status,created_at"
```

---

## ORDER BY Columns

* Include direction (ASC/DESC)
* Preserve order

Example:

```
"created_at DESC,id DESC"
```

---

## LIKE Pattern Type

* `prefix` → `column LIKE 'abc%'`
* `suffix` → `column LIKE '%abc'`
* `full` → `column LIKE '%abc%'`
* `none` → no LIKE

---

## Pagination Type

* `offset` → LIMIT/OFFSET
* `keyset` → cursor/keyset
* `none` → no pagination

---

## Full Scan Risk Estimation

* `high` → leading wildcard LIKE, function on indexed column, weak predicates
* `medium` → partial risk
* `low` → index-aligned filtering and sorting

---

# CSV Safety Rules

* Always wrap SQL in double quotes.
* Escape internal quotes as `""`.
* Prefer single-line SQL.
* Do not add markdown inside the CSV file.

---

# Quality Checklist

For each new entry:

* [ ] `query_id` is unique
* [ ] SQL text is quoted correctly
* [ ] Metadata matches actual SQL structure
* [ ] `file_path` (and `function_or_method`, `line_range` when available) is filled for traceability
* [ ] `execution_context` is set (api/batch/worker/cron/admin)
* [ ] Query structure is deduplicated and normalized
* [ ] Dynamic variants are represented when structure differs

---

This skill ensures a complete, structured SQL inventory extracted from application source code. Index and WHERE proposals are a **separate, optional follow-up**; for reference only, see [references/sql_tuning_proposals_by_table.md](references/sql_tuning_proposals_by_table.md) (not part of this skill's deliverable).
