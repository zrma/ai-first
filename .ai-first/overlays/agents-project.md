## Repository Overlay

- Stage 0부터 Stage 11까지의 release/adoption과 Stage 12의 local 구현·검증을 완료했다.
  published stable과 development candidate는 `docs/HANDOFF.md`에서 구분한다. 계약과 evidence는
  `docs/completed-milestones.md`, 현재 상태와 다음 trigger는
  `docs/HANDOFF.md`와 `docs/status.md`가 소유한다.
- spec 설계 계약과 완료 지식 이관은 `docs/WORK_LIFECYCLE.md`를 따른다.
  현재 active milestone은 `docs/HANDOFF.md`에서 확인한다. 새 milestone이나 bounded
  specification 요구가 생기면 목적·관계·완료 조건을 정립하는 spec을 연다.
- framework core는 model/vendor 중립적으로 유지하고 model별 지침은 교체 가능한
  capability profile로 둔다.
- 소비 저장소는 framework version을 pin하고 생성된 artifact를 tracked 상태로
  보유해 독립 clone에서도 동작해야 한다.
- 다른 저장소 도입은 해당 저장소의 기본 working copy 밖의 VCS-isolated checkout에서
  수행한다. native gate가 Git worktree metadata를 요구하면 Git-backed checkout을
  colocated `jj`로 관리한다.
- 중앙 공개 저장소에는 소비 저장소 inventory, local workspace 경로와 migration
  진행 원문을 기록하지 않는다.
- 전체 local gate는 `scripts/check.sh`, generated drift check는
  `python3 .ai-first/check.py`다.
