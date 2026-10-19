# Handoff

## 현재 단계

현재 published stable은 `v1.10.1`이다. signed source tag와 원격 source identity,
fresh clone의 canonical gate 및 동일 source SHA의 Python 3.11/3.14 CI를 확인했다.
로컬 시작·선형 통합·종료 흐름의 실행 계약은 `docs/VCS_CLOSEOUT.md`가 소유한다.
이전 source/tag/release와 도입 이전 이력은 보존했다.

## 현재 milestone

활성 milestone은 없다. 로컬 VCS lifecycle과 활성 소비 갱신을 검증하고 의도·결정·
한계를 owning artifact로 이관했다. 완료 packet과 active pointer는 제거했다.
release source tag와 이후 완료 문서 main은 구별한다.

선택형 `vcs-closeout`은 start/resume/own/integrate/finish를 제공한다. 시작 기록은
저장소 밖 private 파일이며 native start/finalize에 같은 세션을 전달한다. 종료 시
기존 WIP·workspace·bookmark·tag 보존과 소유 사본의 등록·경로 회수를 대조한다.
standalone은 생성물 무결성만 검사하고 로컬 절차를 CI나 서버 규칙으로 대체하지 않는다.
제품 native CI를 유지하며 공통 VCS 후보 binding만 제거했다.

`verification`은 선택형 보조 기능, `work-coordination`은 실험적 opt-in이다.
기존 profile·overlay·native lifecycle과 model baseline은 유지했다. 자동 삭제·push,
임의 명령의 강제 차단, 외부 clone 전수 발견과 장기 행동 개선은 보증하지 않는다.

## 시작 순서

1. answer/review/plan은 관련 경로에서 시작한다. 변경은 현재 상태와 관련 spec을 읽고
   첫 수정 전 로컬 VCS 세션을 시작한다. 재개는 기존 세션을 resume한다.
2. spec·완료 이관은 `docs/WORK_LIFECYCLE.md`, 검증은 `docs/VERIFICATION.md`를 따른다.
3. publication은 `docs/PUBLICATION.md`의 repository 및 machine-local gate를 통과한다.
4. native 결과, durable history, remote SHA와 사본 회수 후 finish를 확인해 마감한다.

## 검증과 한계

- canonical gate: framework 테스트 102개, real Git/Jujutsu fixture, generated/interface,
  publication, navigation 및 기존 CI contract PASS.
- source: signed annotated `v1.10.1`, remote tag/source equality와 fresh-clone gate PASS.
- 소비 갱신: source/render/standalone, 각 native gate, 선형 후보와 remote head,
  task-owned 사본 회수와 실제 세션 finish를 확인했다. 원격 CI는 private 출고 증거로 별도 대조한다.
- 기존 WIP·고유 북마크·release/tag/배포 자산 identity를 시작 기록과 대조했다.
- native runner의 의도된 내부 skip은 해당 명령의 검증 범위와 구별한다.
- 지침·명령 회귀와 이번 실제 적용의 증거이며 향후 모든 agent의 준수나 재작업·시간·
  비용 감소를 실측한 결과는 아니다. inventory와 raw evidence는 machine-local 계층에 둔다.

## 관련 문서와 후속 조건

구조는 `docs/ARCHITECTURE.md`, 호환성은 `docs/COMPATIBILITY.md`, 완료 결과는
`docs/completed-milestones.md`, 현재 상태는 `docs/status.md`, 다음 trigger는
`docs/roadmap.md`가 소유한다. capability 확대는 반복 운영 근거나 명시적 요구가
있을 때 범위를 정하고 native 계약·권한을 보존한다.
