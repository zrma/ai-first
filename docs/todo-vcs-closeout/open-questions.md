# Open questions

- 기존 merge는 고정된 repository-owned ancestor checkpoint로 보존한다. 이후 새 merge만 거부한다.
- 새 runtime은 선택형 vcs-closeout이며 vcs-jj를 요구한다. 기존 선택형 기능은 추가하지 않는다.
- GitHub branch rule은 repository administration 경계로 남기고 공통 검사를 server enforcement로 보고하지 않는다.
