# Bootstrap Core Open Questions

## Non-blocking

- stable CLI를 Python source, zipapp 또는 native binary 중 무엇으로 배포할지
- profile fragment를 Markdown, TOML metadata 또는 둘의 조합으로 표현할지
- generated file 전체를 합성할지, marker로 관리되는 core block만 합성할지
- stable release에서 compatibility window를 몇 개 version으로 둘지

첫 vertical slice에서는 dependency-free Python standard library, Markdown fragment와
전체 generated output을 사용해 contract를 검증한다. pilot evidence가 반대 방향을
보이면 stable v1 전에 변경할 수 있다.

## Blocking before publication

- license 선택

## Blocking before stable v1

- released framework source를 consumer가 검증하는 content-addressed distribution 형식
- profile 간 conflict와 precedence 규칙
