### openai-agent-guidance

- 현재 OpenAI model과 prompting guidance는 versioned core가 아니라 공식 문서로
  갱신되는 provider capability다.
- model migration은 workload role, endpoint, effective reasoning, tool contract,
  cache와 output contract를 먼저 보존한 뒤 가장 작은 변경으로 수행한다.
- prompt 변경은 대표 task에서 관측된 failure에 연결하고 한 번에 한 종류의
  중복·충돌 또는 누락만 수정한 뒤 같은 evidence로 재검증한다.
- GPT-6 Astra calibration은 공식 [model guide](https://developers.openai.com/api/docs/guides/latest-model)의
  prompting/migration 지침을 2026-09-05에 확인한 기준이다. core 계약을 적용할 때
  다음 model-specific 경향을 조정한다.
  - 승인 질문 때문에 작업이 일찍 멈추면 기존 task 권한과 scope를 먼저 복원하고,
    허용된 준비 작업을 검증 가능한 결과로 만든 뒤 남은 권한 경계에서 질문한다.
  - user instruction은 skill의 일반 가이드보다 우선한다. skill 때문에 중단하거나
    요청을 미완료로 남기면 읽은 `SKILL.md`의 경로와 해당 문구, 적용 이유를 밝히고
    명시된 요구와 해석을 구분한다. core의 권한·공개 경계는 유지한다.
  - 설명은 결과를 먼저 밝히는 간결한 문단을 기본으로 하고 비교·순서가 필요한
    경우 목록을 사용한다. 기술 세부사항은 결론을 이해하는 데 필요한 만큼 쓴다.
  - 검증은 변경 위험에 비례해 필수 repository gate까지 수행한다. 통과한 뒤에는
    새 변경, 실패 또는 미해결 우려가 있을 때만 범위를 넓히거나 반복한다.
  - subagent 사용은 해당 환경의 위임 정책과 task scope를 따른다. profile 채택을
    병렬 agent 실행이나 추가 비용의 승인으로 해석하지 않는다.
- 실제 Astra API migration에서는 tool calling의 Responses API 요구,
  `none`/`minimal` effort의 `low` 전환, unsupported sampling/logprob parameter를
  확인한다. 기존의 다른 effective effort와 workload 역할을 유지하며, endpoint나
  tool handler 변경이 필요하면 별도 implementation 범위를 확정한다.
- Programmatic Tool Calling은 bounded read-only reduction에만 사용하고 approval,
  semantic judgment, citation과 final validation은 direct path에 남긴다.
