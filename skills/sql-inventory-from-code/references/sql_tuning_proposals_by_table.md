# Table-Based SQL Tuning Proposals

This document is generated and maintained based on:

templates/sql_catalog.csv

It organizes SQL analysis and tuning proposals by table.

This document does not apply changes directly.
It documents structured proposals only.

---

# Usage Rules

* Every proposal must reference one or more `query_id` values.
* Original queries (v1) must never be modified.
* If an improved query is proposed, it must be added to the CSV as:

  * `query_version = v2`
  * `mapped_from_query_id = <original query_id>`
* All proposals must include validation steps.

---

# Table: <table_name>

## 1. Current Query Usage Summary

* Referenced Query IDs:

  * QRY-...
* Main query types:

  * SELECT / UPDATE / DELETE / INSERT
* Common WHERE columns:

  * column_a
  * column_b
* Common ORDER BY columns:

  * created_at DESC
* Pagination patterns:

  * offset / keyset / none
* High scan risk queries:

  * QRY-...

---

## 2. Index Proposals

### Proposal ID: IDX-<table>-001

**Target Pattern**

Describe the filtering and sorting pattern this index is intended to support.

Example:

* WHERE status = ?
* AND created_at >= ?
* ORDER BY created_at DESC

**Suggested Index (DDL)**

```sql
CREATE INDEX idx_<table>_<columns>
ON <table> (<column1>, <column2>);
```

**Impacted Queries**

* QRY-...

**Expected Impact**

* Reduce full table scans
* Improve ORDER BY performance
* Reduce rows examined

**Trade-offs**

* Increased storage usage
* Slower INSERT/UPDATE operations
* Additional maintenance overhead

**Validation Steps**

1. Run EXPLAIN before index creation.
2. Create index in staging.
3. Run EXPLAIN again.
4. Compare:

   * Index usage
   * Rows examined
   * Sort operations
   * Execution time

---

## 3. Query Improvement Proposals

### Query: QRY-<id> (v1 → v2)

**Problem Description**

Explain the structural issue:

* Leading wildcard LIKE
* Function on indexed column
* OR-heavy predicate
* Misaligned ORDER BY
* Inefficient pagination

**Original Query (v1)**

```sql
-- Paste from sql_catalog.csv
```

**Improved Query (v2)**

```sql
-- Improved version (same semantics)
```

**Reason for Improvement**

Explain why this version improves performance:

* Better index usage
* Reduced scanned rows
* Avoided filesort
* Removed unnecessary functions

**CSV Update Instructions**

Add a new row in `sql_catalog.csv`:

* query_id = same as original
* query_version = v2
* mapped_from_query_id = <original query_id>
* Update metadata fields accordingly
* Recalculate full_scan_risk

**Validation**

* Confirm result equivalence
* Compare execution plans
* Confirm index usage (if applicable)

---

# Appendix: Common Tuning Patterns

## Composite Index Ordering

1. Equality predicates first
2. Range predicates next
3. ORDER BY columns last (if beneficial)

---

## Anti-Patterns

* Leading wildcard LIKE (`%term%`)
* Functions applied to indexed columns
* Excessive OR conditions
* OFFSET pagination on large datasets
* SELECT * on wide tables

---

## Pagination Recommendation

For large datasets:

* Prefer keyset pagination over OFFSET
* Align ORDER BY with index definition

---

## Inventory Synchronization Rule

Whenever a proposal modifies query structure:

* The improved query must be added to the inventory CSV.
* The original entry must remain unchanged.
* Metadata must stay consistent across documents.

---

End of template.
