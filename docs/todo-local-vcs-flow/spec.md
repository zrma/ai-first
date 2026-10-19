# Local agent VCS workflow

상태: 구현 중

## Problem and outcome

수동 종료 검사와 CI backstop만으로는 agent가 작업 시작 상태와 직접 만든 사본을
연결할 수 없다. change 작업의 시작·선형 통합·종료를 하나의 로컬 기록으로 검증한다.

## Scope and constraints

선택형 vcs-closeout에 dependency-free local lifecycle을 추가하고 generated guidance 및
기존 native start/finalize와 연결한다. 기존 WIP·고유 history·tag/release와 native gate는
보존한다. CI의 자동 history 호출과 그 때문에 추가한 설정만 제거한다.
자동 삭제, 강제 push, server administration, vendor hook, multi-agent coordinator는 범위 밖이다.

## Acceptance

- 첫 수정 전 기존 상태를 저장소 밖에 기록하고 재시작으로 덮어쓰지 않는다.
- 사본 생성 전 소유 경로를 등록하고 종료 시 등록 및 directory 잔여물을 검출한다.
- stale/divergent/merge/conflicted 후보는 bookmark 이동 전에 거부한다.
- 기존 WIP·secondary workspace·unique refs·release tags를 보존한다.
- 완료 후보가 durable하고 empty WC 및 사본 회수와 공유 Git hook의 직접 임시 경로 참조 제거가 확인될 때만 finish가 성공한다.
- real jj/Git fixtures와 native gates, release-source/consumer drift 검사로 검증한다.
- 기존 제품 CI는 보존하고 불필요한 harness CI binding만 제거한다.

## Evidence boundary

명령 회귀와 이번 rollout의 실제 수행 증거를 구별한다. 지침 준수가 임의 명령 실행을
강제로 차단하거나 향후 모든 agent 작업의 무결성을 보증한다고 주장하지 않는다.

## Observed correction

실제 rollout의 package prepare가 공유 Git hook에 task 경로를 남겼다. 경로 회수만으로
마감이 통과하던 누락을 1.10.1에 보완하고 실제 canonical hook을 복구했다.
