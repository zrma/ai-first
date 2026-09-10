### verification

`verification`은 standalone `.ai-first/verify.py`와 repository-scoped
`.agents/skills/ai-first-verify/SKILL.md`를 배포한다. repository-owned binding
`.ai-first/verification.toml`이 native runner 또는 선택한 toolchain 기본 명령을 연결한다.
`--plan`은 discovery와 범위를, `--run`은 결과를, `--report FILE`은 현재 소스와의
freshness를 제공한다. 제품 acceptance, 외부 실행 권한과 native lifecycle은 소유하지 않는다.
