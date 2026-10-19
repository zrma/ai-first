### Capability Profile: vcs-closeout

- `vcs-jj`와 함께 선택하며 generated `python3 .ai-first/vcs.py`로 기본 bookmark와
  반영 후보의 선형 이력을 검사한다. standalone check는 history 검사만 포함한다.
- 과거 이력의 병합을 보존해야 하면 repository-owned `[vcs].linear_history_base`를
  full commit ID로 고정한다. 그 기준점은 후보의 조상이어야 하며 이후 새 병합은 거부한다.
- 작업을 마칠 때 `python3 .ai-first/vcs.py --closeout`으로 empty working copy와
  expected parent, workspace/head/Git 등록과 task-owned 경로의 회수를 별도로 확인한다.
- 보존할 기존 작업은 시작 전에 기록한 정확한 working-copy ID, head와 workspace로
  명시한다. 검사를 통과시키려고 기존 WIP를 재작성·삭제하거나 새 사본을 inherited로
  분류하지 않는다. 종료 검사와 server-side branch rule을 같은 검증으로 보고하지 않는다.
