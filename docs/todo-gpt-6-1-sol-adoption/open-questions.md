# Open questions

## 결정된 범위

- target은 GPT-6.1 Sol (`gpt-6.1-sol`)이며 일반 latest resolver로 대체하지 않는다.
- capability guidance 변경은 backward-compatible minor `1.8.0`으로 준비한다.
- 추가 기능 선택과 제품 runtime 변경은 포함하지 않는다.

## 남은 publication 경계

local 준비·검증 후 framework main/signed tag 및 소비 저장소별 push의 정확한 action과
target에 대한 권한을 확인한다. 이전 완료 task의 publication 권한을 새 version에
자동 적용하지 않는다.
