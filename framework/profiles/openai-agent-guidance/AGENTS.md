### Capability Profile: openai-agent-guidance

- OpenAI model, API, prompt 또는 agent guidance를 변경하기 전에는 `openai-docs`
  workflow가 있으면 사용하고, 공식
  [latest model guide](https://developers.openai.com/api/docs/guides/latest-model)와
  해당 model의 migration/prompting guide를 현재 source of truth로 확인한다.
- 이 version의 agent guidance baseline은 GPT-6 Astra (`gpt-6-astra`)다. 명시된
  model target은 보존하고, current/latest 요청은 공식 문서로 다시 확인한다.
  application runtime model string은 기존 integration point와 workload role을
  확인하지 않고 변경하지 않는다.
- prompt는 outcome, success criteria, permission, evidence와 stopping condition을
  보존하고, core와 중복되는 generic process instruction을 추가하지 않는다.
- Astra의 승인 질문, skill instruction 해석과 검증 범위는 harness profile의
  calibration을 따른다. skill의 일반 권장을 추가 승인 조건으로 해석하지 않는다.
- Pro mode, Programmatic Tool Calling, persisted reasoning, async tools, mid-turn
  steering과 multi-agent behavior는 관측된 문제나 명시적 요구가 있을 때 별도
  capability change로 평가한다.
