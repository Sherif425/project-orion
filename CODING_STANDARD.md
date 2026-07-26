# Coding Standard

## Purpose

This document defines the coding standards followed throughout Project Orion.

The goal is to produce Python code that is readable, maintainable, and professional.

---

# General Principles

Code should be:

* Simple
* Readable
* Modular
* Consistent
* Maintainable

Readable code is preferred over clever code.

---

# Style Guide

Project Orion follows:

* PEP 8
* Meaningful variable names
* Meaningful function names
* Type hints where appropriate
* Docstrings for public modules, classes, and functions

---

# Project Structure

Applications should be organized into logical modules.

Avoid large files that mix unrelated responsibilities.

---

# Functions

Functions should:

* Perform one task
* Be easy to test
* Return predictable results
* Handle errors appropriately

---

# Error Handling

Use exceptions responsibly.

Never ignore unexpected errors.

Provide meaningful error messages.

---

# Logging

Use Python's `logging` module instead of `print()` for application logging.

`print()` is acceptable for simple learning exercises and CLI output.

---

# Configuration

Configuration should be stored outside the source code whenever practical.

Avoid hard-coded credentials.

Use environment variables for secrets.

---

# Testing

Where appropriate:

* Write unit tests.
* Test edge cases.
* Keep tests independent.
* Ensure tests are reproducible.

---

# Code Review Checklist

Before committing code:

* Is it readable?
* Does it follow PEP 8?
* Is unnecessary duplication removed?
* Are errors handled correctly?
* Is documentation updated?
* Have tests been executed (where applicable)?
