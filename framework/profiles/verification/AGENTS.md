### Capability Profile: verification

- 변경 검증과 완료 보고에는 `.agents/skills/ai-first-verify/SKILL.md`를 사용한다.
- `python3 .ai-first/verify.py --plan`으로 연결된 검증과 coverage를 확인하고
  승인된 범위의 `--run`으로 실행한다. native runner의 내부 명령을 별도로 복제하지 않는다.
- binding과 discovery는 권한을 부여하지 않는다. 명령 성공과 제품 시나리오 충족을
  구분하고 skip·stale·미검증을 결과에 반영한다.
