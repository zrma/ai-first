### Capability Profile: vcs-jj

- local VCS는 `jj`를 사용하고 상태, diff, log, bookmark와 remote를 각각 확인한다.
- change description은 `<type>: <summary>`와 configured attribution policy를 따른다.
- 의미 있고 검증된 logical unit은 `jj describe`로 provenance를 갖춘 설명을 설정한 뒤
  `jj new`로 새 empty working-copy change를 만들어 닫는다. 사용자가 no-commit을
  지시하거나 repository가 금지하는 경우가 아니면 이를 기본 local closeout으로 수행한다.
- 여러 logical unit은 하나의 mutable working-copy change에 누적하지 않는다. blocker로
  미완료 WIP를 남기면 격리하고 이유와 resume point를 보고한다.
- publication permission이 없는 상태에서는 default bookmark를 이동하지 않는다. 승인된
  publication transaction에서만 intended change로 bookmark를 옮기고 push한다.
- 다른 작업과 migration은 기본 working copy 밖의 VCS-isolated checkout으로
  격리한다. `jj workspace`를 우선하되 native gate가 실제 Git worktree metadata를
  요구하면 Git-backed checkout을 colocated `jj`로 관리한다.
- `rebase`, `squash`, `split`, `abandon`과 published bookmark 이동은 명시적인
  history-mutation permission을 요구한다.
- 기본 bookmark 통합은 선형 이력을 유지하며 stale push나 동시 변경을 새 merge로
  우회하지 않는다. 최신 remote 위에 미출고 변경을 선형으로 재적용하고 검증한다.
  기존 published history와 release ref는 별도 승인 없이 재작성하지 않는다.
- publication은 fail-fast로 실행한다. push 거절이나 대상 SHA 불일치를 해결하기 전에
  tag/release 등 후속 mutation을 실행하지 않는다. finalize helper도 기본값으로
  default bookmark를 이동하지 않으며 성공 뒤 새 empty working copy를 확인한다.
- task가 만드는 workspace/worktree/별도 clone을 생성 시점부터 task-local 범위에
  기록한다. 완료·실패 뒤에는 소유한 사본의 unique work·등록·실제 경로를 각각 확인해
  회수하고, 다른 active/WIP와 기존 고유 이력은 보존한다.
