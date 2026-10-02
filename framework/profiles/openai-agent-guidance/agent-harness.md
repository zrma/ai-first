### openai-agent-guidance

- 현재 OpenAI model과 prompting guidance는 versioned core가 아니라 공식 문서로
  갱신되는 provider capability다.
- model migration은 workload role, endpoint, effective reasoning, tool contract,
  cache와 output contract를 먼저 보존한 뒤 가장 작은 변경으로 수행한다.
- prompt 변경은 대표 task에서 관측된 failure에 연결하고 한 번에 한 종류의
  중복·충돌 또는 누락만 수정한 뒤 같은 evidence로 재검증한다.
- baseline은 GPT-6.1 Sol (`gpt-6.1-sol`)이다. 공식
  [model guide](https://developers.openai.com/api/docs/guides/latest-model)와
  [Sol model page](https://developers.openai.com/api/docs/models/gpt-6.1-sol)를
  2026-10-02에 확인했다. 아래 GPT-6 family prompting 지침은 Astra에서 관측한 행동을
  출발점으로 제시한 것이며 Sol의 동일한 경향이나 개선 효과가 실측됐다는 뜻은 아니다.
  선택한 model과 workload에서 관측된 문제에 맞춰 core 계약 적용을 조정한다.
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
- 실제 GPT-6.1 Sol API migration에서는 tool calling에 Responses API를 사용한다.
  Chat Completions는 tool 없는 요청에만 사용한다. reasoning effort는 `low`,
  `medium` (기본값), `high`, `xhigh`, `max`를 지원하며 기존 effective effort를
  가능한 한 보존한다. `none`/`minimal`은 지원하지 않으므로 `low`에서 대표 task를
  비교한다. `temperature`, `top_p`, `top_logprobs`를 제거하고, Chat Completions의
  `logprobs`와 Responses include의 `message.output_text.logprobs`도 확인한다.
  endpoint나 tool handler 변경이 필요하면 별도 implementation 범위를 확정한다.
- Programmatic Tool Calling은 bounded read-only reduction에만 사용하고 approval,
  semantic judgment, citation과 final validation은 direct path에 남긴다.
