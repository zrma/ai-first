---
name: ai-first-work
description: 독립 변경을 여러 agent에게 나누거나 격리된 단일 작업을 시작할 때 workspace 준비, 수정 범위, 검증 인계와 통합을 실행한다. work-coordination profile과 jj가 있는 저장소에서 사용하며 일반 질의나 순서 의존성이 있는 편집을 병렬 작업으로 확대하지 않는다.
---

# Isolated work and integration

native spec에서 목표와 성공 조건을 확인하고 이번 작업에서 수정할 파일/디렉터리를
정한다. 공통 CLI가 workspace와 인계·통합 상태를 처리하므로 이를 위한 별도 wrapper나
수동 manifest를 만들지 않는다. 다른 파일은 읽을 수 있지만 배정 범위 밖의 편집은
coordinator에게 돌려보낸다. 범위 검사는 사후 acceptance gate이며 OS sandbox가 아니다.

## Coordinator

1. `python3 .ai-first/verify.py --plan`에서 현재 native 검증 연결을 확인한다.
   runner가 없으면 discovery의 실행 가능한 기본 후보를 검토·연결한다.
2. repository 밖의 새 디렉터리로 work를 연다.
   `python3 .ai-first/work.py init --state <private-state> --objective <outcome> --write <paths...>`
3. 독립 작업마다 `assign --state <private-state> --id <task-id> --objective <outcome>
   --write <paths...>`를 실행한다. 필요한 경우 `--check <ids...>`로 worker의 검증 범위를
   제한한다. 같은 경로를 쓰거나 순서 의존성이 있는 작업은 순차로 나눈다.
4. 반환된 packet을 host의 agent 호출에 전달한다. Codex에서는 packet의 workspace,
   목표·수정 범위·검증 범위와 repository 지침을 subagent에게 전달한다. 원래 승인된
   작업 경계와 사용 가능한 host budget을 유지한다. CLI가 agent를 자동 호출하지 않는다.
5. worker가 준비되면 `handoff --state <private-state> --id <task-id>`가 실제 revision과
   수정 범위를 검사하고 배정된 검증을 실행한다. worker의 완료 문장만으로 넘어가지 않는다.
6. 모두 인계된 뒤 `integrate --state <private-state>`를 실행한다. 별도 clone에 변경을
   합치고 전체 연결 검증을 실행한다. 반환된 workspace/revision에서 원래 요청의
   acceptance와 제품 동작을 검토한다. `verified`는 연결한 검증의 성공이며 publication이나
   인간 acceptance가 아니다. 통합 결과의 채택은 기존 local VCS/native lifecycle을 따른다.

## Worker

packet의 workspace에서 repository 지침을 읽고 배정 범위 안에서 변경한다. 다른 worker의
workspace와 공유 state 파일을 직접 수정하지 않는다. 필요한 읽기·검증도 원래 작업 권한을
따르며 secret·external write 권한은 packet에서 생기지 않는다.
native 규칙에 따라 logical change를 설명하고, 실제 변경과 남은 쟁점을 coordinator에게
인계한다. `handoff`가 배정된 검증을 수행하므로 같은 검증을 불필요하게 반복하지 않는다.

## 실패와 재개

`status --state <private-state>`와 `packet --state <private-state> --id <task-id>`로
현재 작업과 재개 자료를 회수한다. agent가 중단됐으면 host에서 이전 실행이 멈췄음을
확인한 뒤 `resume --state <private-state> --id <task-id>`로 재배정한다. 진행 중인 검증을
살려 둔 채 resume하지 않는다. interrupted integration에는 id 없이 resume한 뒤
integrate를 다시 실행한다. 이전 workspace와 결과는 보존된다.

source가 진전됐거나 worker가 인계 후 바뀌면 자동 rebase/재통합하지 않는다. 실제 diff와
의존성을 검토해 현행 기준의 새 work를 시작한다. CLI는 workspace나 local bookmark를
자동 삭제하지 않는다. 다른 agent vendor의 호출 호환성은 각 adapter를 실제 검증하기
전에는 주장하지 않는다.
