### Capability Profile: vcs-jj

- local VCS는 `jj`를 사용하고 상태, diff, log, bookmark와 remote를 각각 확인한다.
- change description은 `<type>: <summary>`와 configured attribution policy를 따른다.
- 다른 작업과 migration은 기본 working copy 밖의 VCS-isolated checkout으로
  격리한다. `jj workspace`를 우선하되 native gate가 실제 Git worktree metadata를
  요구하면 Git-backed checkout을 colocated `jj`로 관리한다.
- `rebase`, `squash`, `split`, `abandon`과 published bookmark 이동은 명시적인
  history-mutation permission을 요구한다.
