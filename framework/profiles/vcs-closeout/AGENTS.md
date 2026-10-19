### Capability Profile: vcs-closeout

- change/build/fix의 첫 수정·작업 사본 생성 전에 `python3 .ai-first/vcs.py start
  --state <private-session-file>`을 canonical workspace에서 실행한다. 이어지는 모든
  단계에 같은 `AI_FIRST_VCS_SESSION`을 설정한다. answer/review에는 시작 기록을 강제하지 않는다.
- 기록은 저장소 밖 private 파일이며 기존 WIP·workspace·head·bookmark·tag를 보존하는
  기준이다. 재개 시 기존 기록을 사용하고 새 start로 덮어쓰거나 이번 작업을 inherited로
  등록하지 않는다. 기존 native start-work/readiness는 이 시작 기록 뒤에 실행한다.
- 새 workspace/worktree/clone은 만들기 전에 canonical root에서 `python3 .ai-first/vcs.py
  own --path <new-task-copy>`로 기록하고 VCS 격리한다. 기존 WIP 위에 작업을 누적하지 않는다.
- 검증·description 이후 통합 직전에 `python3 .ai-first/vcs.py integrate --revision
  <candidate>`를 실행한다. publication 승인 시 fetch 후 `--remote origin`도 지정한다.
  현재 main과 최신 remote 위의 선형 후보만 허용하며 stale 상태는 merge로 우회하지 않는다.
- native finalize는 위 통합 검사를 bookmark 이동 전에 연결하고, 출고 권한·공개 gate를
  별도로 지킨다. helper 성공만으로 마감하지 않는다. 작업 결과에 durable bookmark를 남기고
  task-owned 사본의 고유 결과·등록·실제 경로를 확인한 뒤 회수한다.
  package prepare가 공유 Git hook을 바꿨다면 canonical hook을 복구하고 임시 경로 참조도 제거한다.
- canonical root에서 `python3 .ai-first/vcs.py finish`가 성공해야 완료를 보고한다.
  실패·중단이면 기록과 WIP를 보존하고 이유·재개점을 남긴다. 도구는 자동 삭제·push를 하지 않는다.
- 과거 병합은 고정 `[vcs].linear_history_base` 이전에 보존하고 기존 release/history를
  재작성하지 않는다. standalone/CI는 입력과 생성물 무결성만 검사하며 로컬 마감을 대체하지 않는다.
