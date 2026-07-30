# Completed Milestones

## Charter and architecture

AI-first를 command-only assistance가 아닌 active project stewardship로 정의했다.
인간은 목적, 방향, 가치, 우선순위와 중요한 결정을 소유하는 방향지시자, 동반자와
project manager로 참여한다.

identity, core, capability profile, repository overlay와 machine-private overlay를
분리하고 소비 저장소의 독립 실행 및 dedicated migration workspace 계약을 고정했다.

검증: `scripts/check.sh`

## Self-hosting core

`0.1.0-dev` 선언, deterministic composition, content-addressed lock, generated
`AGENTS.md`/agent harness, central drift check와 standalone checker를 구현했다.

synthetic consumer fixture가 동일 입력의 결정성, manual output와 overlay drift,
unsafe path, symlink escape와 framework checkout 없는 standalone 검증을 증명한다.

검증: `scripts/check.sh`

## Public foundation

`Apache-2.0` license, public README/contribution/security policy, least-privilege CI와
repository publication checker를 구성했다.

repository gate와 권한 있는 machine-local `all` gate를 통과한 동일 commit을 public
`main`에 게시하고 visibility, default branch, local/remote equality와 Python
3.11/3.14 terminal CI를 검증했다. private vulnerability reporting도 활성화했다.

검증: `scripts/check.sh`, public remote metadata와 terminal CI
