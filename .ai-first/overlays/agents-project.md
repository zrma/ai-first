## Repository Overlay

- 현재 milestone은 `docs/todo-representative-pilots/`가 소유한다.
- framework core는 model/vendor 중립적으로 유지하고 model별 지침은 교체 가능한
  capability profile로 둔다.
- 소비 저장소는 framework version을 pin하고 생성된 artifact를 tracked 상태로
  보유해 독립 clone에서도 동작해야 한다.
- 다른 저장소 도입은 해당 저장소의 기본 working copy가 아니라 전용 `jj workspace`에서
  수행한다.
- 중앙 공개 저장소에는 소비 저장소 inventory, local workspace 경로와 migration
  진행 원문을 기록하지 않는다.
- 전체 local gate는 `scripts/check.sh`, generated drift check는
  `python3 .ai-first/check.py`다.
