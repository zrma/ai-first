#!/bin/sh
# shellcheck disable=SC2016
set -eu

repo_root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repo_root"

fail() {
  printf 'agent harness interface check failed: %s\n' "$*" >&2
  exit 1
}

for required_file in \
  AGENTS.md \
  CONTRIBUTING.md \
  LICENSE \
  README.md \
  SECURITY.md \
  docs/AI_FIRST_CHARTER.md \
  docs/ARCHITECTURE.md \
  docs/agent-harness.md \
  docs/HANDOFF.md \
  docs/status.md \
  docs/roadmap.md \
  docs/completed-milestones.md \
  docs/PUBLICATION.md \
  docs/REPO_MANIFEST.yaml \
  docs/WORK_LIFECYCLE.md; do
  [ -s "$required_file" ] || fail "missing or empty $required_file"
done

# 공통 version/source/profile/interface 검사는 배포된 checker가 소유한다.
python3 .ai-first/check.py

grep -Fq -- 'AI는 command-only assistant가 아니라' AGENTS.md ||
  fail "AI-first identity is missing from AGENTS.md"
grep -Fq -- '방향지시자, 동반자와 project manager' docs/AI_FIRST_CHARTER.md ||
  fail "human role is missing from the charter"
grep -Fq -- 'VCS-isolated migration checkout' docs/ARCHITECTURE.md ||
  fail "VCS-isolated migration checkout boundary is missing"
grep -Fq -- 'Git-backed checkout' framework/profiles/vcs-jj/AGENTS.md ||
  fail "Git metadata fallback is missing from vcs-jj profile"
grep -Fq -- 'empty working-copy change' AGENTS.md ||
  fail "logical local VCS closeout is missing"
grep -Fq -- 'task-local publication authorization' docs/agent-harness.md ||
  fail "task-local publication authorization is missing"
grep -Fq -- 'Scope proportionality' AGENTS.md ||
  fail "investigation-depth proportionality is missing"
grep -Fq -- 'contract/status review' docs/agent-harness.md ||
  fail "contract review scope guard is missing"
grep -Fq -- '`gpt-6-astra`' AGENTS.md ||
  fail "current OpenAI model guidance is missing"

printf 'agent harness interface check passed\n'
