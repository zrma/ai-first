### Capability Profile: openai-agent-guidance

- OpenAI model, API, prompt 또는 agent guidance를 변경하기 전에는 `openai-docs`
  workflow가 있으면 사용하고, 공식
  [latest model guide](https://developers.openai.com/api/docs/guides/latest-model)와
  해당 model의 migration/prompting guide를 현재 source of truth로 확인한다.
- current/latest OpenAI model이 명시적 target인 agent guidance에는
  `gpt-5.6-sol`을 사용한다. application runtime model string은 기존 integration
  point와 workload role을 확인하지 않고 변경하지 않는다.
- prompt는 outcome, success criteria, permission, evidence와 stopping condition을
  보존하고, core와 중복되는 generic process instruction을 추가하지 않는다.
- Pro mode, Programmatic Tool Calling, persisted reasoning과 multi-agent behavior는
  관측된 문제나 명시적 요구가 있을 때 별도 capability change로 평가한다.
