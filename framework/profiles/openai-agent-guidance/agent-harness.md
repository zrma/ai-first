### openai-agent-guidance

- 현재 OpenAI model과 prompting guidance는 versioned core가 아니라 공식 문서로
  갱신되는 provider capability다.
- model migration은 workload role, endpoint, effective reasoning, tool contract,
  cache와 output contract를 먼저 보존한 뒤 가장 작은 변경으로 수행한다.
- prompt 변경은 대표 task에서 관측된 failure에 연결하고 한 번에 한 종류의
  중복·충돌 또는 누락만 수정한 뒤 같은 evidence로 재검증한다.
- Programmatic Tool Calling은 bounded read-only reduction에만 사용하고 approval,
  semantic judgment, citation과 final validation은 direct path에 남긴다.
