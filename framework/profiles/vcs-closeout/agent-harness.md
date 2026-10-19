### vcs-closeout

- history: `python3 .ai-first/vcs.py`; 후보는 `--revision <revision>`으로 지정한다.
- CI의 standalone checker는 `AI_FIRST_VCS_REVISION`이 있으면 실제 후보 SHA를 사용한다.
  GitHub PR의 synthetic merge 대신 head SHA를 전달하고 full history를 fetch한다.
- closeout: `python3 .ai-first/vcs.py --closeout`; 출고 후 기본 bookmark의 parent를
  확인하고 local-only 마감은 `--revision <completed-revision>`을 사용한다.
- 다른 활성 workspace/head/Git worktree는 `--keep-workspace`, `--keep-head`,
  `--keep-worktree`로 분류하고 기존 working copy는 `--inherited-working-copy`에
  시작 시점의 정확한 commit ID를 지정해 보존한다. task가 만든 임시 사본은
  `--retired-path`로 모두 열거한다. 검사는 읽기와 working-copy snapshot만 수행한다.
