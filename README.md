# SQL-Like Query Engine in Python (File-Backed Mini DBMS)

## Overview

This repository contains a **SQL-like query engine** implemented in Python to demonstrate core relational database behavior: **creating schemas, manipulating records, filtering with predicates, joining tables, and committing changes under a simplified transaction model**. The engine stores data in the filesystem (directories and text files) so that query execution and persistence are easy to inspect.

> Scope note: this is an educational engine that supports a **defined subset of SQL**, not a full ANSI SQL implementation.

---

## What this project demonstrates (SQL-focused)

* **Schema and table management (Data Definition Language):** create/drop databases, create/alter/drop tables
* **Record operations (Data Manipulation Language):** insert, update, delete, and select rows
* **Filtering:** `WHERE` conditions with basic comparisons
* **Relational joins:** inner join and left outer join using table aliases and equality predicates
* **Transactions (simplified):** `BEGIN TRANSACTION` + `COMMIT` with file-based locking and commit-time persistence

---

## Implementation overview

### Storage model (filesystem-backed)

* **Database** → directory
* **Table** → text file

  * first line: schema (column names)
  * subsequent lines: records (rows)

### Execution flow

1. Read SQL-like statements (terminated by `;`)
2. Parse tokens (subset grammar)
3. Dispatch to operation handlers (schema operations, record operations, joins, transactions)
4. Read/modify table rows and persist to disk (or defer until commit)

---

## Supported SQL subset

### Data Definition Language

* `CREATE DATABASE <name>;`
* `DROP DATABASE <name>;`
* `USE <name>;`
* `CREATE TABLE <table> (...);`
* `ALTER TABLE <table> ADD COLUMN <col>;`
* `DROP TABLE <table>;`

### Data Manipulation Language

* `INSERT INTO <table> VALUES (...);`
* `SELECT ... FROM <table> [WHERE ...];`
* `UPDATE <table> SET <col> = <value> WHERE ...;`
* `DELETE FROM <table> WHERE ...;`

### Joins

* Implicit join: `SELECT ... FROM T1 A, T2 B WHERE A.x = B.y;`
* Explicit join forms:

  * `INNER JOIN`
  * `LEFT OUTER JOIN`
* Join predicate: equality (`=`) with table aliases

### Transactions (simplified)

* `BEGIN TRANSACTION;`
* `COMMIT;`
* File-based locking to prevent conflicting writes; changes are persisted at commit time

---

## How to run

```bash
python3 P4.py
```

* Enter commands interactively
* End each statement with `;`
* Exit with `.exit`

---

## Minimal end-to-end example (covers major features once)

```sql
CREATE DATABASE company;
USE company;

CREATE TABLE employees (id, name, dept_id);
CREATE TABLE departments (id, dept_name);
ALTER TABLE employees ADD COLUMN title;

INSERT INTO employees VALUES (1, Alice, 10, Engineer);
INSERT INTO departments VALUES (10, Engineering);

SELECT name, title FROM employees WHERE dept_id = 10;

UPDATE employees SET title = SeniorEngineer WHERE id = 1;
DELETE FROM employees WHERE id = 999;

SELECT * FROM employees E INNER JOIN departments D ON E.dept_id = D.id;

BEGIN TRANSACTION;
INSERT INTO employees VALUES (2, Bob, 10, Intern);
COMMIT;
```

---

## Project structure

* **P1.py** — schema/database/table management (Data Definition Language), basic selection
* **P2.py** — record operations (Data Manipulation Language) + conditional selection
* **P3.py** — join execution (inner join and left outer join)
* **P4.py** — transaction handling with file-based locking and commit persistence

---

## Limitations (intentional scope)

* Subset SQL grammar (token-based parsing; limited quoting/format flexibility)
* No indexes or query optimizer
* No aggregates (`GROUP BY`, `COUNT`, etc.) or ordering (`ORDER BY`)
* Simplified transaction model (illustrative locking; no rollback / write-ahead logging)
* Each file represents an individual project component; the functionalities have not yet been fully integrated into a single execution flow, which will be added in a future update

---

## Author

**Yeamin Chowdhury**
