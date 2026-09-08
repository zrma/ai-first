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

stable release는 `1.5.0`이다. milestone/bounded specification의 목적, 조건과 관계를
todo spec으로 정립하고, 완료 시 지속할 지식을 소유 artifact로 이관한 뒤 작업 문서를
정리하는 계약을 제공한다. model/vendor 중립적인 core와 기존 schema/Structure ID,
GPT-6 Astra (`gpt-6-astra`) capability profile을 유지한다.

선언에서 core, capability profile과 repository overlay를 결정적으로 합성하고,
central framework check와 standalone consumer drift check가 같은 lock을 검증한다.
완료 packet의 active namespace 잔류를 막는 lifecycle gate, logical VCS closeout과
bounded-task permission continuity도 유지한다.

signed annotated `v1.5.0`의 서명과 remote tag identity, Python 3.11/3.14 CI를 검증했다.
승인된 활성 소비 저장소의 release pin 전환도 repository별 native/publication gate,
remote equality와 same-SHA terminal CI까지 완료했다. 완료 범위와 evidence는
[`완료 요약`](docs/completed-milestones.md)에 있다.

기존 완료 spec의 설계 근거와 후속 조건을 architecture, compatibility와 lifecycle
문서로 이관하고 원본 작업 packet을 정리했다. 원본 보존은 명시적인 추적·운영 필요가
있을 때 선택한다.

현재 development candidate `1.6.0-dev`는 기존 spec의 의도·제약과 spec 변경 자체를
리뷰에 연결하고, 완료 후에도 당시 기준과 최종 소유 문서를 추적하는 계약을 제공한다.
문서량과 리뷰 깊이는 위험에 비례하며 기존 native 형식과 schema를 유지한다.
local 합성·회귀 검증을 완료했으며 release와 소비 저장소 adoption은 아직 수행하지 않았다.

현재 사실과 다음 순서는 [`docs/HANDOFF.md`](docs/HANDOFF.md), 장기 방향은
[`docs/roadmap.md`](docs/roadmap.md)를 따른다.

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
