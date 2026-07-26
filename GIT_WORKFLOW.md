# Git Workflow

## Purpose

This document defines the Git workflow used throughout Project Orion.

---

# Branch Strategy

The default branch is:

```
main
```

Feature work may be developed in short-lived branches before merging into `main`.

Example:

```
feature/database-backup
feature/pandas-analysis
feature/api-client
```

---

# Commit Messages

Commit messages should describe the purpose of the change.

Examples:

```
Add database backup utility

Implement CSV parser

Refactor logging module

Fix API authentication bug
```

Avoid messages such as:

```
update

changes

fix

test
```

---

# Daily Workflow

```bash
git status

git add .

git commit -m "Meaningful description"

git push
```

---

# Before Every Commit

Verify:

* Code works.
* Documentation is updated.
* Tests pass (if available).
* No temporary files are included.

---

# Repository Hygiene

Do not commit:

* Secrets
* Passwords
* API keys
* Virtual environments
* Cache files
* Generated binaries

Use `.gitignore` appropriately.

---

# Release Philosophy

Small, frequent commits are preferred over infrequent, very large commits.

Each commit should represent one logical improvement.
