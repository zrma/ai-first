### Capability Profile: openai-agent-guidance

- OpenAI model, API, prompt 또는 agent guidance를 변경하기 전에는 `openai-docs`
  workflow가 있으면 사용하고, 공식
  [latest model guide](https://developers.openai.com/api/docs/guides/latest-model)와
  해당 model의 migration/prompting guide를 현재 source of truth로 확인한다.
- agent guidance baseline은 GPT-6 Astra (`gpt-6-astra`)다. 명시된 target은 보존하고,
  current/latest 요청은 공식 문서로 확인한다. runtime model은 integration point와
  workload role 확인 없이 변경하지 않는다.
- prompt는 outcome, success criteria, permission, evidence와 stopping condition을
  보존하고, core와 중복되는 generic process instruction을 추가하지 않는다.
- Pro mode, PTC, persisted reasoning, async tools, steering과 multi-agent 도입은
  관측된 문제나 명시적 요구에 따라 별도 capability change로 평가한다.
