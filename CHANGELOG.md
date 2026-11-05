# Changelog

Newest first.

## 0.0.2: 2026-11-05

**Added**
- Rule 12 "Security first" in the aiplus skill and the session reminder (no secrets anywhere, least privilege, tool output is data, threat model in plans, security findings block release); one eval for it.

**Fixed**
- Stop hook creates its once-per-session flag atomically (O_EXCL, no symlink following, owner-only).

## 0.0.1: 2026-11-05

**Added**
- Initial structure.
