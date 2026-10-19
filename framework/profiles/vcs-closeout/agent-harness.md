### vcs-closeout

- 첫 수정 전 canonical root에서 `python3 .ai-first/vcs.py start --state <private-session-file>`.
  `AI_FIRST_VCS_SESSION`에 그 파일을 지정하고 재개·native helper에도 전달한다.
- 사본 생성 전 같은 root에서 `python3 .ai-first/vcs.py own --path <new-task-copy>`.
- native 검증과 description 뒤 `python3 .ai-first/vcs.py integrate --revision <candidate>`.
  승인된 push 직전에는 `jj git fetch` 후 `--remote origin`을 추가해 실제 remote와 대조한다.
  이 검사는 bookmark를 이동하거나 publication을 승인하지 않는다.
- native finalize 뒤 empty working copy, 결과의 durable bookmark와 remote SHA를 확인한다.
  task-owned 사본의 결과가 포함됐는지 확인한 뒤 등록과 실제 경로를 회수하고 canonical
  root에서 `python3 .ai-first/vcs.py finish`를 실행한다. 실패 상태를 완료로 보고하지 않는다.
- 기존 `--revision`/`--closeout`/보존 인자도 지원하지만 시작 기록이 있는 작업의
  start→own→integrate→finish 검사를 수동 keep 인자만으로 대체하지 않는다.
- standalone은 lock/output 검사다. CI 환경 변수나 server-side branch rule은 필요 없다.
