### vcs-jj

- 시작 evidence는 `jj status`, `jj diff`, 최근 `jj log`와 workspace/bookmark 관계다.
- 각 검증된 logical unit에 attribution이 포함된 description을 설정하고 `jj new`로
  empty working-copy change를 만든다. 다음 unit을 시작하기 전에 이 closeout을 수행한다.
- publication permission이 없으면 default bookmark와 remote를 그대로 두고 exact
  pending action을 보고한다. 승인된 transaction이면 bookmark, push, remote identity와
  terminal CI를 중간 재승인 없이 닫는다.
- 다른 작업과 겹치는 변경은 기본 working copy 밖의 VCS-isolated checkout과 독립
  change로 분리한다. 격리 방식은 repository-native Git/Jujutsu metadata gate를
  그대로 통과해야 한다.
- push 성공은 remote bookmark가 의도한 commit을 가리키는지로 검증한다.
- empty working-copy change, unbookmarked head와 stale workspace를 같은 잔여물로
  취급하지 않는다.
