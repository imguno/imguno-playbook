# imguno-playbook

Reusable AI engineering skills and playbooks for production use.

Skills in this repo are ready to plug into AI-assisted workflows (e.g. Cursor, custom agents). Each skill is a self-contained set of instructions, templates, and references—scoped by responsibility and designed to grow with your systems.

---

## What’s in this repo

- **Skills** — Step-by-step playbooks for specific engineering tasks (e.g. building a SQL inventory from code, documenting APIs, analyzing performance). Each skill lives under `skills/<skill-name>/` with a `SKILL.md`, optional `templates/`, and `references/`.
- **Playbooks** — Structured workflows that combine clarity, traceability, and safety so they can be used in real environments.

Use them as-is or adapt them to your stack and conventions.

---

## Principles

Skills here are:

- **Scoped** — Clear boundaries and a single primary deliverable per skill.
- **Versioned** — Changes are tracked; history and compatibility matter.
- **Structured** — Consistent layout (SKILL.md, templates, references) so tools and humans can navigate them.
- **Production-minded** — No destructive defaults; optional steps and follow-ups are explicit.
- **Extensible** — New skills can be added without tying the repo to one domain (SQL, APIs, docs, etc.).

---

## Skills

<!-- SKILLS:START -->
- **[Sql Inventory From Code](skills/sql-inventory-from-code/SKILL.md)** — Collects and maintains a complete CSV-based SQL query inventory (SSOT) by extracting all SQL statements from a service application's source code. This skill's only deliverable is the inventory CSV. Use when extracting SQL from application source code, building a query inventory from the codebase, or preparing for SQL tuning from code.
<!-- SKILLS:END -->

Additional skills (e.g. API documentation, performance analysis, system docs) will be added over time.

---

## Layout

```
skills/
└── <skill-name>/
    ├── SKILL.md          # Main instructions and scope
    ├── templates/        # Output templates (e.g. CSV, markdown)
    └── references/       # Optional reference docs
```

---

## Contributing

When adding or changing skills, keep scope and deliverable clear, document assumptions, and avoid destructive or environment-specific defaults so the playbook stays reusable across teams and repos.
