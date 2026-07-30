#!/bin/sh
set -eu

repo_root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repo_root"

fail() {
  printf 'agent harness interface check failed: %s\n' "$*" >&2
  exit 1
}

for required_file in \
  AGENTS.md \
  README.md \
  docs/AI_FIRST_CHARTER.md \
  docs/ARCHITECTURE.md \
  docs/agent-harness.md \
  docs/HANDOFF.md \
  docs/status.md \
  docs/roadmap.md \
  docs/PUBLICATION.md \
  docs/REPO_MANIFEST.yaml \
  docs/todo-bootstrap-core/spec.md \
  docs/todo-bootstrap-core/open-questions.md; do
  [ -s "$required_file" ] || fail "missing or empty $required_file"
done

expected_agents_headings=$(cat <<'HEADINGS'
## First Read
## AI-first Core Contract
## Repository Overlay
HEADINGS
)
actual_agents_headings=$(sed -n 's/^\(## .*\)$/\1/p' AGENTS.md)
[ "$actual_agents_headings" = "$expected_agents_headings" ] ||
  fail "AGENTS.md section order differs from the bootstrap map"

for required_line in \
  '- Structure ID: `ai-first-harness-v1`.' \
  '- Framework version: `0.1.0-dev`.' \
  '- Convergence stage: `bootstrap`.' \
  '- Target stage: `self-hosting`.' \
  '- Canonical check: `scripts/check-agent-harness-interface.sh`.' \
  '- Publication class: `public`.'; do
  grep -Fq -- "$required_line" docs/agent-harness.md ||
    fail "docs/agent-harness.md is missing: $required_line"
done

expected_harness_headings=$(cat <<'HEADINGS'
## Interface
## Project Objective
## Source Of Truth
## Autonomy And Permissions
## Execution Loop
## Verification And Evidence
## Escalation
## VCS And Publish
## Harness Evaluation And Improvement
## Framework Overlay
## Related Documents
HEADINGS
)
actual_harness_headings=$(sed -n 's/^\(## .*\)$/\1/p' docs/agent-harness.md)
[ "$actual_harness_headings" = "$expected_harness_headings" ] ||
  fail "docs/agent-harness.md section order differs from ai-first-harness-v1"

grep -Fq -- 'AI는 command-only assistant가 아니라' AGENTS.md ||
  fail "AI-first identity is missing from AGENTS.md"
grep -Fq -- '방향지시자, 동반자와 project manager' docs/AI_FIRST_CHARTER.md ||
  fail "human role is missing from the charter"
grep -Fq -- '전용 migration workspace' docs/ARCHITECTURE.md ||
  fail "migration workspace boundary is missing"

printf 'agent harness interface check passed\n'
