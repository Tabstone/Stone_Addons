# TabS Cleaner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first TabS Cleaner Home Assistant add-on with a CleanMyMac-style UI, storage scan, safe automatic cleanup, selected deep cleanup, and audit history.

**Architecture:** The add-on is a self-contained Python standard-library HTTP server serving static HTML/CSS/JS and JSON APIs. Backend actions are strict allowlists around Docker, HA CLI, and mapped filesystem scans. The UI calls scan and cleanup endpoints and presents storage health, safe findings, deep findings, and history.

**Tech Stack:** Home Assistant add-on metadata, Alpine base image, Python 3 standard library, Docker CLI, HA CLI when available, static HTML/CSS/JavaScript, Python unittest.

---

### Task 1: Add Backend Core and Tests

**Files:**
- Create: `tabs-cleaner/rootfs/opt/tabs_cleaner/core.py`
- Create: `tabs-cleaner/tests/test_core.py`

- [ ] **Step 1: Write tests for cleanup planning**

Run: `python3 -m unittest tabs-cleaner/tests/test_core.py -v`

Expected: FAIL because `tabs_cleaner.core` does not exist.

- [ ] **Step 2: Implement core helpers**

Implement:

- `SAFE_CLEAN_ACTIONS`
- `DEEP_CLEAN_ACTIONS`
- `human_bytes`
- `risk_level`
- `build_safe_plan`
- `build_deep_plan`
- `summarize_storage`

- [ ] **Step 3: Run tests**

Run: `python3 -m unittest tabs-cleaner/tests/test_core.py -v`

Expected: all tests pass.

### Task 2: Add HTTP Server

**Files:**
- Create: `tabs-cleaner/rootfs/opt/tabs_cleaner/server.py`

- [ ] **Step 1: Add API server**

Expose:

- `GET /api/status`
- `POST /api/scan`
- `POST /api/clean/safe`
- `POST /api/clean/deep`
- `GET /api/history`

- [ ] **Step 2: Add command runner guardrails**

Ensure all shell commands are built server-side from allowlisted action IDs. User input can select actions and backup slugs, but cannot provide raw commands.

### Task 3: Add CleanMyMac-Style Frontend

**Files:**
- Create: `tabs-cleaner/rootfs/opt/tabs_cleaner/static/index.html`
- Create: `tabs-cleaner/rootfs/opt/tabs_cleaner/static/styles.css`
- Create: `tabs-cleaner/rootfs/opt/tabs_cleaner/static/app.js`

- [ ] **Step 1: Build dashboard layout**

Include sidebar modules, storage ring, scan button, status cards, safe review, deep review, and history.

- [ ] **Step 2: Wire UI to API**

Implement scan, safe cleanup, selected deep cleanup, and history loading.

### Task 4: Add Add-on Packaging

**Files:**
- Create: `tabs-cleaner/config.yaml`
- Create: `tabs-cleaner/build.yaml`
- Create: `tabs-cleaner/Dockerfile`
- Create: `tabs-cleaner/run.sh`
- Create: `tabs-cleaner/rootfs/etc/cont-init.d/20-folders.sh`
- Create: `tabs-cleaner/rootfs/etc/cont-init.d/99-run.sh`
- Create: `tabs-cleaner/DOCS.md`
- Create: `tabs-cleaner/CHANGELOG.md`
- Create: `tabs-cleaner/icon.png`
- Create: `tabs-cleaner/logo.png`

- [ ] **Step 1: Add metadata**

Configure ingress, Docker API, Supervisor API, admin role, data mappings, and options.

- [ ] **Step 2: Add runtime scripts**

Install and run the Python server on port `8099`.

### Task 5: Update Repository Docs and Verify

**Files:**
- Modify: `README.md`
- Modify: `README_CN.md`

- [ ] **Step 1: Add TabS Cleaner to README tables**

- [ ] **Step 2: Run tests**

Run: `python3 -m unittest discover -s tabs-cleaner/tests -v`

Expected: all tests pass.

- [ ] **Step 3: Run metadata smoke checks**

Run: `python3 -m unittest discover -s tests -v`

Expected: existing repository tests pass.
