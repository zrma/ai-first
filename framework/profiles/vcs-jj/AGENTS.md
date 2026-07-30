### Capability Profile: vcs-jj

- local VCS는 `jj`를 사용하고 상태, diff, log, bookmark와 remote를 각각 확인한다.
- change description은 `<type>: <summary>`와 configured attribution policy를 따른다.
- 다른 작업과 migration은 전용 `jj workspace`로 격리한다.
- `rebase`, `squash`, `split`, `abandon`과 published bookmark 이동은 명시적인
  history-mutation permission을 요구한다.
