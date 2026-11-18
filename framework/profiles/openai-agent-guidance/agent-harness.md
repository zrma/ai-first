### openai-agent-guidance

- 현재 OpenAI model과 prompting guidance는 versioned core가 아니라 공식 문서로
  갱신되는 provider capability다.
- model migration은 workload role, endpoint, effective reasoning, tool contract,
  cache와 output contract를 먼저 보존한 뒤 가장 작은 변경으로 수행한다.
- prompt 변경은 대표 task에서 관측된 failure에 연결하고 한 번에 한 종류의
  중복·충돌 또는 누락만 수정한 뒤 같은 evidence로 재검증한다.
- baseline은 GPT-6.2 Sol (`gpt-6.2-sol`)이다. 공식
  [model guide](https://developers.openai.com/api/docs/guides/latest-model)와
  [Sol model page](https://developers.openai.com/api/docs/models/gpt-6.2-sol)를
  2026-11-19에 확인했다. 공식 GPT-6.2 공통 프롬프트 예시를 출발점으로 삼고,
  선택한 모델과 대표 작업에서 확인한 결과로 적용 효과를 판단한다.
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
- 실제 GPT-6.2 Sol API migration에서는 tool calling에 Responses API를 사용한다.
  Chat Completions는 tool 없는 요청에 사용하고 기존 effective effort를 가능한 한
  보존한다. 새 통합은 `medium`에서 시작한다. Responses는 `reasoning.effort`, Chat Completions는
  `reasoning_effort`로 지정한다. `none`/`minimal`은 지원하지 않으므로 `low`에서
  대표 task를 비교한다. `temperature`, `top_p`, `top_logprobs`와 Chat Completions의
  `logprobs`를 제거하고, Responses의 `include`에서 `message.output_text.logprobs`
  항목도 제거한다.
  endpoint나 tool handler 변경이 필요하면 별도 implementation 범위를 확정한다.
- GPT-6.2 Responses는 top-level `instructions`를 `input` 뒤에 붙이며 해당 토큰은
  uncached input으로 과금한다. 여러 턴에 재사용하는 지침은 `input`의 첫 `developer`
  메시지에 두고, 현재 요청에만 적용할 지침은 `instructions`로 전달한다.
- 대화가 이어질 때 기존 prefix는 그대로 재생하고 지침 변경은 새 `developer` 메시지로
  추가한다. 이전 메시지나 tool 결과를 수정하면 그 이후 추론 항목이 제거될 수 있다.
  `input_transformations`에서 추론 항목 제거 여부를 확인한다. 모델이나 사용자·조직이
  바뀌는 경우에도 추론 재사용을 전제하지 않는다. 세부 규칙은 공식
  [prefix 보존 가이드](https://developers.openai.com/api/docs/guides/keep-prefix-unchanged)를 따른다.
- GPT-5.5 이하에서 옮길 때 기존 요청의 `prompt_cache_retention`을
  `prompt_cache_options.ttl: "30m"`으로 전환한다. GPT-6.2 Sol의 cache read는
  uncached input의 5%이며, cache write는 `30m`이면 1.25배, Responses의 `12h`면
  2.5배로 과금한다. cache hit와 write 비용을
  함께 비교한다. cache 경계와 재사용 조건은 공식
  [prompt caching 문서](https://developers.openai.com/api/docs/guides/prompt-caching#summary-of-model-differences)를 따른다.
- 대화 중 effort 변경을 도입할 때는 standard single-agent Responses의
  `configuration_update`를 검토하고 원래 request-level effort를 유지한다.
  `context_management`는 compaction 뒤 최신 update를 다시 내보낸다. automatic
  truncation과 standalone `/responses/compact`는 update가 포함된 history를 거부한다.
  standalone compaction이 필요하면 최신 update 값을 따로 보존하고, compaction 요청에서
  update 항목을 빼고, 반환된 window 뒤에 재적용한다. 응답의 `reasoning.effort`는
  request-level 값이다. 공식 [reasoning 가이드](https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation)와
  [compaction 가이드](https://developers.openai.com/api/docs/guides/compaction#continue-with-configuration-updates-and-tools)를 따른다.
- GPT-6.2 Sol의 US/EU data residency는 Standard, Fast, Batch에서 지원된다.
  Ultrafast의 data residency는 US만 지원한다. `service_tier: "ultrafast"` 도입 전에
  공식 [Ultrafast 문서](https://developers.openai.com/api/docs/guides/ultrafast-mode)에서
  비용·rate limit을, [data residency 문서](https://developers.openai.com/api/docs/guides/data-residency#which-models-and-features-are-eligible-for-data-residency)에서 리전 조건을 확인한다.
- 이 framework의 Programmatic Tool Calling 운영 정책은 bounded read-only reduction으로
  제한하고 approval, semantic judgment, citation과 final validation은 direct path에 남긴다.
