# ai-first

`ai-first`는 AI가 지시를 기다리는 보조 도구에 머무르지 않고, 명시된 방향과
경계 안에서 프로젝트를 능동적으로 꾸려 나가도록 만드는 공개 프로젝트 운영
프레임워크다.

AI는 맥락 복원, 다음 과제 발견, 계획, 구현, 검증, 문서화와 인계를 맡는다.
인간은 목적, 방향, 가치, 우선순위와 중요한 결정을 소유하며 방향지시자,
동반자와 프로젝트 매니저로 참여한다.

## 목표

- 모델과 기술 스택에 종속되지 않는 AI-first 정체성과 운영 계약을 정의한다.
- 공통 core, 선택 가능한 capability profile과 repository overlay를 합성한다.
- 생성된 저장소가 framework checkout 없이도 독립적으로 이해되고 검증되게 한다.
- framework 갱신을 버전 고정, diff 검토와 repository-local gate로 통제한다.
- 공개 artifact와 machine-private 운영 정보를 명확히 분리한다.

## 현재 상태

`1.7.0`은 공통 interface 검사를 standalone checker에 모아 framework 갱신 때 native
assertion을 반복 수정하는 비용을 줄인다. 소비 저장소는 기존 profile 선택과 제품 고유
검증을 유지하며 version/source pin과 generated artifact를 갱신한다.

[검증 workflow](docs/VERIFICATION.md)는 필요할 때 선택하는 보조 기능이다.
[작업 배정·통합 도구](docs/WORK_COORDINATION.md)는 독립 worker의 범위·revision·재개 관리가
필요한 경우를 위한 실험적 opt-in이다. 소비 저장소 갱신 시 새 runtime이나 binding을
일괄 추가하지 않는다. 작은 작업은 기존 native 명령과 흐름으로 수행한다.

model/vendor 중립적인 core, 기존 schema/Structure ID와 GPT-6 Astra
(`gpt-6-astra`) capability profile을 유지한다. 선언에서 core, profile과 overlay를
결정적으로 합성하며 central/standalone check가 같은 lock을 검증한다.
기존 spec의 의도·제약·acceptance와 diff/evidence를 대조하고 완료 지식을 owning artifact로
이관하는 계약도 유지한다.

기능별 실행 검증과 실측 효용의 차이, 추가 호출 비용과 작은 표본의 한계는
[완료 요약](docs/completed-milestones.md)에 있다. 현재 publication/adoption 상태와
다음 순서는 [handoff](docs/HANDOFF.md), 장기 방향은 [roadmap](docs/roadmap.md)을 따른다.

## 설계 원칙

- **Self-contained consumer:** 생성된 저장소는 중앙 저장소나 sibling 경로 없이
  clone 직후 동작해야 한다.
- **Pinned core:** 소비 저장소는 framework version과 입력 digest를 고정한다.
- **Repository-owned overlay:** 제품 목적, source of truth, domain invariant와
  검증 명령은 소비 저장소가 소유한다.
- **Evidence over ceremony:** 파일 존재보다 AI가 프로젝트를 실제로 전진시키고
  검증 가능한 결과를 남기는지를 평가한다.
- **Explicit boundaries:** external write, 파괴적 변경, 비용, secret와 제품 방향
  결정은 명시적인 인간 판단 경계다.
- **No live path coupling:** symlink, submodule 또는 machine-local sibling path를
  실행 전제로 삼지 않는다.

## 문서 지도

- AI-first 정체성: [`docs/AI_FIRST_CHARTER.md`](docs/AI_FIRST_CHARTER.md)
- architecture와 합성 경계: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- v1 compatibility와 source pin: [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md)
- 공통 실행·증거 workflow: [`docs/VERIFICATION.md`](docs/VERIFICATION.md)
- 독립 작업 배정·인계·통합: [`docs/WORK_COORDINATION.md`](docs/WORK_COORDINATION.md)
- agent operating loop: [`docs/agent-harness.md`](docs/agent-harness.md)
- 공개 경계: [`docs/PUBLICATION.md`](docs/PUBLICATION.md)
- 완료 milestone 요약:
  [`docs/completed-milestones.md`](docs/completed-milestones.md)
- spec 정립과 완료 지식 이관: [`docs/WORK_LIFECYCLE.md`](docs/WORK_LIFECYCLE.md)
- 기여: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- 보안: [`SECURITY.md`](SECURITY.md)

## 검증

```sh
scripts/check.sh
```

현재 선언을 다시 합성하거나 drift를 확인하려면 다음 명령을 사용한다.

```sh
scripts/ai-first render --repo .
scripts/ai-first check --repo .
python3 .ai-first/check.py
```

최초 공개 전에는 repository publication gate와 권한 있는 machine-local
private-inventory gate를 모두 실행한다.

## License

이 프로젝트는 [Apache License 2.0](LICENSE)에 따라 배포된다.
