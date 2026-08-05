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
