---
name: differential_pr_security_review
description: Security-focused differential review of PRs, commits, and diffs using git blame, blast-radius caller counts, regression checks, and post-patch validation.
domain: cybersec_audit
provenance: curated from trailofbits/differential-review and trailofbits/post-patch-validation (CC-BY-SA-4.0)
---
# Differential PR Security Review

## When to Use
Use before merging PRs, validating security patches, or checking if a refactor silently re-introduced a fixed bug or broke an invariant.

## 1. Scope & Risk Triage
- Run `rtk git diff --stat` and `rtk git log -n 5 --oneline` to classify diff size (`SMALL < 200 LOC`, `MEDIUM`, `LARGE`).
- Prioritize review order: (1) auth/session/permissions, (2) crypto/tokens/secrets, (3) SQL/file/shell/network sinks, (4) schema/input parsers, (5) dependencies/CI workflows.

## 2. Blast Radius & Historical Context
- For every modified exported function, search callers (`ast-grep` or `rg`) to measure blast radius and check whether callers depend on previously enforced preconditions.
- Run `rtk git log -S "<symbol>" -p -n 3` or `git blame` on deleted guards/checks to ensure a historical security fix is NOT being removed accidentally.

## 3. Post-Patch Verification
- Verify the patch fixes the **root cause** (not just a single symptom string).
- Check for missing negative tests: every security fix requires at least one automated test proving the vulnerable input is now rejected and benign inputs still succeed.
- Run `uv run run-gates` and report explicit coverage boundaries (files reviewed vs. skipped) and confidence level.
