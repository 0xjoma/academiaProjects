# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A collection of cryptography and cybersecurity assignments from a Master's in Cybersecurity program. Each top-level directory is an independent, self-contained project—there is no shared build system, monorepo tooling, or cross-project dependencies.

## Languages & Runtimes

- **Python 3.12+** — used by most projects. Some projects have a local `.venv/` (e.g., `module_01_coding_assignment_the_erastosthenes_method/`). Run scripts directly: `python3 <script>.py`
- **TypeScript/React** — `risk_management_project_timeline/` uses React + D3 for a Gantt chart. Install deps with `npm install` in that directory.

## Project Map

| Directory | Topic | Key Files |
|---|---|---|
| `module_01_*` | Sieve of Eratosthenes (prime generation) | `ortiz_perez_primes.py` |
| `module_02_*` | Number generators (RNG) | `number_generators.py` |
| `module_03_*_part_1_*` | Block ciphers (Part A) | `P3a.py`, `StringConversion.py` |
| `module_03_*_part_2_*` | Block ciphers (Part B) | `P3b.py`, `StringConversion.py` |
| `aes_assignment_2/` | AES implementation | `AES_Project.py` |
| `l3_dlp_programming_assignment/` | Discrete log / ElGamal | `bsgs.py`, `elgamal_break.py` |
| `l5_pollard_p1_assignment/` | Pollard's p-1 factoring | `pollard_p1.py` |
| `l6_hash_libsha_1_programming_assignment/` | SHA-1 / SHA-3 hashing | `hashlib_hashes.py`, `SHA1.py` |
| `final_project_deliverable_1/` | DES implementation | `DES.py`, `StringConversion.py` |
| `final_project_deliverable_2/` | RSA implementation | `RSA.py`, `StringConversion.py` |
| `final_project_deliverable_3/` | MMO hash function | `MMO.py`, `StringConversion.py` |
| `final_project_deliverable_5/` | Secure messaging (RSA+DES) | `secure_messaging.py` |
| `risk_management_project_timeline/` | Gantt chart (React/D3) | `risk-management-gantt.tsx` |

## Shared Pattern: StringConversion.py

`StringConversion.py` is a utility module duplicated across several projects (`module_03_*`, `final_project_deliverable_1–3`). It provides hex/binary/string conversion helpers used by the cryptographic implementations. Each copy is local to its project directory.

## Running Projects

Each Python project runs standalone from its own directory:
```bash
cd <project_dir>
python3 <main_script>.py
```

No test framework is configured. No linter or formatter is enforced repo-wide.
