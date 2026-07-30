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

현재는 bootstrap 단계다. 정체성, architecture와 첫 self-hosting milestone이
정의되어 있으며 합성 도구와 standalone consumer contract는 구현 중이다.

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
- agent operating loop: [`docs/agent-harness.md`](docs/agent-harness.md)
- 공개 경계: [`docs/PUBLICATION.md`](docs/PUBLICATION.md)
- 현재 milestone: [`docs/todo-bootstrap-core/spec.md`](docs/todo-bootstrap-core/spec.md)

## 검증

```sh
scripts/check.sh
```

공개 remote와 license는 아직 확정되지 않았다. 최초 공개 전에는 repository
publication gate와 권한 있는 machine-local private-inventory gate를 모두 실행한다.
