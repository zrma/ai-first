# Open questions

blocking question은 없다.

- optional profile의 고정 output path로 기존 schema를 보존한다. binding은 선택형
  repository input이며 native runner를 단일 argv로 연결한다.
- 자동 discovery의 후보는 명시적으로 선택한 후 binding으로 저장한다. 명령 선택과
  실행을 분리해 문서 존재만으로 native full gate를 실행하지 않는다.
- local report 파일은 명시한 repository 외부 위치에만 새로 쓴다. 기본 출력은 JSON이다.
- 실행 결과는 선언한 coverage에 관한 evidence이며 제품 acceptance 자동 판정이 아니다.
