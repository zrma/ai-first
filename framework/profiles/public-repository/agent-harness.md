### public-repository

- repository-local checker는 generic leak pattern과 content class를 검증한다.
- machine-local checker는 live visibility와 권한 있는 private inventory 대조를
  담당하며 inventory를 repository나 CI에 저장하지 않는다.
- CI는 push 이후 backstop이며 최초 공개 노출을 막는 주 gate가 아니다.
- 최초 공개와 history rewrite 뒤에는 current tree뿐 아니라 reachable history와
  release surface까지 검사한다.
