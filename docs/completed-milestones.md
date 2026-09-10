# Completed Milestones

아래는 각 작업 종료 당시 기록한 결과와 검증 범위다. 현재 계약은 architecture,
compatibility와 `docs/WORK_LIFECYCLE.md`가 소유하며 원래 작업 spec은 VCS 이력으로
추적한다. 과거 성공 기록은 현재 remote/runtime 상태의 재검증을 뜻하지 않는다.

## Charter and architecture

AI-first를 command-only assistance가 아닌 active project stewardship로 정의했다.
인간은 목적, 방향, 가치, 우선순위와 중요한 결정을 소유하는 방향지시자, 동반자와
project manager로 참여한다.

identity, core, capability profile, repository overlay와 machine-private overlay를
분리하고 소비 저장소의 독립 실행 및 VCS-isolated migration checkout 계약을 고정했다.

검증: `scripts/check.sh`

## Self-hosting core

`0.1.0-dev` 선언, deterministic composition, content-addressed lock, generated
`AGENTS.md`/agent harness, central drift check와 standalone checker를 구현했다.

synthetic consumer fixture가 동일 입력의 결정성, manual output와 overlay drift,
unsafe path, symlink escape와 framework checkout 없는 standalone 검증을 증명한다.

검증: `scripts/check.sh`

## Public foundation

`Apache-2.0` license, public README/contribution/security policy, least-privilege CI와
repository publication checker를 구성했다.

repository gate와 권한 있는 machine-local `all` gate를 통과한 동일 commit을 public
`main`에 게시하고 visibility, default branch, local/remote equality와 Python
3.11/3.14 terminal CI를 검증했다. private vulnerability reporting도 활성화했다.

검증: `scripts/check.sh`, public remote metadata와 terminal CI

## Representative pilots

서로 다른 개발·운영·publication class의 대표 흐름에서 pinned core, generated
artifact, repository overlay와 standalone drift check를 도입했다.

각 repository-native canonical gate와 publication boundary를 보존하고 remote commit
equality와 terminal CI까지 독립적으로 검증했다. native gate가 실제 Git worktree
metadata를 요구할 때는 Git-backed isolated checkout을 colocated `jj`로 관리하는
fallback과 repository-owned todo/closure lifecycle 보존 규칙을 framework에 환류했다.

검증: framework self-hosting gate, 소비 저장소 canonical gate와 terminal CI

## Stable v1

framework/schema/Structure ID의 compatibility 축을 분리하고 `1.0.0` self-hosting
identity를 고정했다. commit source와 stable annotated release source는 clean checkout
및 실제 commit을 검증하고 lock에 `source_commit`을 기록한다.

release-ready commit의 Python 3.11/3.14 CI를 확인한 뒤 signed annotated `v1.0.0`
tag를 게시했다. local/remote tag object, peeled commit과 서명을 확인하고 실제
release-source consumer render 및 standalone check를 통과시켰다.

검증: `scripts/check.sh`, signed tag verification, remote tag identity, terminal CI

## Portfolio adoption

승인된 소비 저장소 집합을 stable `v1.0.0` pin, repository-owned overlay와 generated
standalone artifact 위에 저장소별 독립 change로 정립했다.

각 대상의 native canonical gate와 publication class를 보존하고 remote default-branch
commit equality 및 same-SHA terminal CI까지 독립적으로 확인했다. 대상 inventory,
local checkout과 진행 원문은 machine-local coordination에만 남겨 공개 framework의
tracked artifact 경계를 유지했다.

검증: `scripts/check.sh`, 소비 저장소별 canonical/publication gate, remote equality와
terminal CI

## Active-work lifecycle

terminal 상태로 닫힌 work packet이 active namespace와 pointer에 남는 문제를
framework contract와 deterministic standalone gate로 차단했다. Markdown status
field와 status heading 형식을 함께 검사하고 active namespace 밖의 completed
history는 허용한다.

signed annotated `v1.1.1` patch release를 게시하고 승인된 소비 저장소 집합을 같은
source identity로 갱신했다. 저장소별 native gate와 publication boundary를 보존한
채 완료 packet을 archive하고 remote default-branch equality와 same-SHA terminal
CI를 확인했다. 대상 inventory와 local coordination 원문은 tracked artifact에
기록하지 않았다.

검증: `scripts/check.sh`, signed tag verification, 소비 저장소별 canonical gate,
remote equality와 terminal CI

## VCS closeout and permission continuity

change/build/fix의 기본 local 종료 상태를 described logical change와 empty working
copy로 고정하고, local closeout과 external publication permission을 분리했다. exact
plan에 대한 승인을 bounded-task authorization으로 유지하되 target, owner, version,
visibility, material scope, destructive history, cost와 secret 경계가 바뀔 때만
재승인하도록 core와 `vcs-jj` profile에 반영했다.

signed annotated `v1.2.0` source와 central terminal CI를 확인한 뒤 승인된 소비 저장소
집합을 같은 source identity로 갱신했다. 저장소별 native/publication gate, remote
default-branch equality와 same-SHA terminal CI를 확인하고 active pointer를 제거했다.
대상 inventory와 local coordination 원문은 tracked artifact에 기록하지 않았다.

검증: `scripts/check.sh`, signed tag verification, 소비 저장소별 canonical/publication
gate, remote equality와 terminal CI

## Contract audit hardening

일반 contract/status review를 capability availability만으로 exhaustive scan, 제품 코드
전수 조사 또는 material time/token/cost 작업으로 확대하지 않는
investigation-depth proportionality를 core에 고정했다.

standalone checker가 `.ai-first.toml`과 lock의 framework source identity, profile 순서,
`framework_inputs` path/digest 형식과 aggregate digest를 비교하게 했다. synthetic
fixture가 config과 lock의 source/profile 불일치와 framework input aggregate 불일치를
거부하고, 기존 stable consumer interface는 변경 없이 통과했다.

검증: focused tampering fixture, self-hosting render/check, `scripts/check.sh`, consumer
standalone/harness interface compatibility

## Stable v1.3 release and adoption

contract audit hardening을 signed annotated `v1.3.0`으로 공개한 뒤 generated Markdown
formatter 호환성 gap을 immutable `v1.3.1` patch로 교정했다. `v1.3.0` tag는 이동하지
않고 signed `v1.3.1` tag의 local/remote identity, peeled commit, 서명과 terminal
Python CI를 검증했다.

승인된 소비 저장소 집합을 `v1.3.1` release source로 갱신하고 저장소별 standalone,
native와 publication gate, remote default-branch equality와 same-SHA terminal CI를
확인했다. 대상 inventory와 local coordination 원문은 tracked artifact에 기록하지
않았다.

검증: `scripts/check.sh`, signed tag verification, 소비 저장소별 canonical/publication
gate, remote equality와 terminal CI

## GPT-6 Astra guidance and adoption

공식 Astra migration/prompting 지침을 `openai-agent-guidance` profile에 반영했다.
승인 질문, skill 해석과 설명·검증 범위를 조정하면서 core의 model/vendor 중립성과
schema/Structure ID를 유지했다. bootstrap은 짧은 routing map으로 두고 상세 model
calibration은 harness에서 제공한다.

signed annotated `v1.4.0` source의 서명, remote tag/commit identity와 terminal Python
CI를 확인했다. 승인된 활성 소비 저장소 집합은 overlay와 기존 작업을 보존하는
격리 checkout에서 release pin을 갱신하고 standalone/native/publication gate,
remote equality와 same-SHA terminal CI까지 검증했다. 대상 inventory와 local
coordination 원문은 tracked artifact에 기록하지 않았다.

검증: `scripts/check.sh`, signed tag verification, 소비 저장소별 canonical/publication
gate, remote equality와 terminal CI. model 행동에 대한 별도 실측 eval은 포함하지 않았다.

## Spec-to-artifact lifecycle

`1.5.0` core에 milestone/bounded specification의 목적·조건·관계·완료 기준 정립,
구현 중 정합성 유지와 완료 지식 이관을 반영했다. 중요한 판단 근거와 한계를 소유
artifact에 남긴 뒤 작업 spec과 질문 파일을 정리한다. 원본 보존은 명시적인 추적·
운영 필요가 있을 때 선택하며 자동 폴더 이동이나 일률적인 별도 보고서를 요구하지
않는다.

기존 완료 packet의 설계 선택은 `docs/ARCHITECTURE.md`, 후속 capability 조건은
`docs/COMPATIBILITY.md`, 운영 lifecycle은 `docs/WORK_LIFECYCLE.md`로 이관했다.
과거 결과와 검증 범위는 이 문서에 유지하고 원본 spec·질문 파일은 정리했다. 소비
저장소의 기존 native 절차는 보존하면서 checklist 중심의 설명을 spec 정립과 지식
이관으로 보충했다. bootstrap 길이 제한은 상세 정책의 소유 문서로 안내해 유지했다.

signed annotated `v1.5.0`의 서명, local/remote tag object와 source commit identity,
source와 같은 SHA의 terminal Python CI를 확인했다. 갱신된 원격 main 위에서 승인된
활성 소비 저장소의 선언·lock·generated artifact·native assertion을 같은 release
source로 전환했다. 저장소별 native/publication gate, remote main equality와
same-SHA terminal CI를 검증했다. 기존 제품 작업과 원본 보존 근거가 있는 기록은
보존했다. 대상 inventory와 local coordination 원문은 machine-local 계층에 둔다.

release 작업의 지속할 결과는 이 문서와 compatibility/handoff/status에 이관하고
active spec·질문 파일과 pointer를 정리했다. source tag는 immutable하게 유지하며
이후 상태 문서 closeout은 별도 main commit이다.

검증: `scripts/check.sh`, signed tag verification, 소비 저장소별 standalone/interface,
native/publication gate, remote equality와 same-SHA terminal CI. 검증은 지침 합성·
문서 정합성과 repository-native gate를 대상으로 하며 model 행동의 실측 eval이나
별도 요청이 없는 live runtime acceptance를 의미하지 않는다.

## Intent-aware change review

`1.6.0`은 기존 spec에 문제·원하는 결과·영향·제약·non-goal을 구별하고,
원래 기준과 이후 spec 변경을 diff·검증과 함께 검토하도록 구체화했다. 유지해야 할
동작의 위반, 근거 없는 기준 완화와 실제 효과의 미검증을 구별하는 시나리오는
`docs/WORK_LIFECYCLE.md`에 있다. PR이 없는 local change에도 같은 리뷰 기준을
적용하며, 완료 후 당시 spec이 필요하면 immutable commit과 경로로 참조한다.

원래 설계와 acceptance의 이력 전용 참조:
`b7979bf31557c7340573f722dfe2aaa78be920ae:docs/todo-intent-review/spec.md`.
해당 기준선은 release source의 공개 이력에서 확인할 수 있다.
기준을 완화하지 않고 결과를 대조했으며, 현재 규칙과 예시는 `docs/WORK_LIFECYCLE.md`,
native 형식·schema의 호환성과 release 경계는 `docs/COMPATIBILITY.md`로 이관했다.
역할이 끝난 packet과 active pointer를 정리했다.

별도 intent 파일과 중앙 readiness schema를 추가하면 native lifecycle과 중복되므로
공통 정보·검토 계약을 generated guidance에 배포하는 방식을 선택했다. 기존 native
packet과 overlay의 render 전후 보존, packet 제거 후 standalone 실행, 중앙 문서 없이
두 generated entrypoint에 리뷰 계약이 전달되는 것을 synthetic fixture로 검사했다.
독립 리뷰에서 발견한 합성 assertion 누락도 보완했다.

signed annotated `v1.6.0`의 서명, local/remote tag object와 source commit identity,
GitHub Release 및 동일 source SHA의 Python 3.11/3.14 CI를 확인했다. release/adoption의
원래 acceptance는
`c6da34456412cb7956b5f0d03011500664f25fca:docs/todo-release-1.6/spec.md`에 있다.
승인된 활성 소비 저장소에서 최종 release pin, standalone/interface와 native gate,
publication boundary, remote equality 및 same-SHA terminal CI까지 검증했다.

native work-start 안내는 기존 spec 안에서 의도를 구체화하도록 연결했다. 실제 생성,
readiness·질문 스키마 및 기존 파일 보존을 확인했으며 기존 active packet과 overlay를
보존했다. 초기 schema PASS는 의미적 요구사항 확정을 대신하지 않는다는 경계를
native 소유 문서에 남겼다. concise routing 검사에서는 공통 생성 본문 증가와 native
안내 예산을 구별하고 기존 native 예산을 유지했다. 별도 중앙 parser는 추가하지 않았다.

검증: `scripts/check.sh`의 25개 unit test, central/standalone drift, harness interface,
repository publication boundary와 navigation PASS. 원래 spec과 diff의 계약 검토,
독립 리뷰와 repository-native 검증을 수행했다. 결과·판단 근거·검증 한계를 이 문서와
`docs/WORK_LIFECYCLE.md`, `docs/COMPATIBILITY.md`에 이관하고 완료 packet을 정리했다.
agent의 실제 발견률·오탐률, 제품 release와 live runtime 배포는 이번 검증에 포함하지
않았다. 지침의 배포와 구조적 정합성이 행동 성능 향상의 실측 evidence를 뜻하지 않는다.


## Reusable verification workflow — local candidate

`1.7.0-dev`에 선택형 `verification` profile을 구현했다. 하나의 stdlib runtime을
central CLI와 standalone consumer에 배포하고, 공통 검증 skill도 version/lock으로
관리한다. native runner 하나를 argv/coverage binding으로 연결하거나 지원 toolchain의
실제 기본 명령을 발견·선택할 수 있다. 실행 실패·skip·도구 부재·timeout·subset과
source freshness를 JSON으로 처리하며 제품별 의미·acceptance와 native lifecycle은
소비 저장소에 남긴다. 사용법과 API 한계는 `docs/VERIFICATION.md`, 계층은
`docs/ARCHITECTURE.md`, 선택형 도입·제거 호환성은 `docs/COMPATIBILITY.md`가 소유한다.

원래 acceptance의 이력 전용 참조:
`acda896a89bdb26ebf83b1822d9119013ef2d882:docs/todo-verification-workflow/spec.md`.
원래 목적은 소비자마다 검증 절차·wrapper·skill을 다시 작성하는 부담을 줄이는 것이었다.
실행 가능한 공통 제공물은 구현했지만, 기존 직접 실행 절차보다 수작업이 줄었다는
효과까지 입증하지는 못했다. 이 차이를 acceptance 완화나 성공 주장으로 덮지 않는다.

### 실행과 도입 검증

canonical gate와 전체 44개 unit test가 통과했다. 추가된 19개 runtime/profile test는
실패·skip·unavailable·timeout, subset, mutation/stale/report 재사용, binding 오류,
private report 저장 경계, standalone 실행, generated drift와 collision/opt-out 보존을
검사한다. 기존 profile 미선택 fixture도 통과했다.

이질적인 기존 consumer 두 곳의 격리 checkout에서 native 문서 gate와 manifest quick
runner를 연결·실행했다. 각각 7줄 binding과 기존 native interface pin 파일 한 곳의
갱신이 필요했고 새 wrapper나 수동 작성 skill은 없었다. 초기 pin 불일치를 native gate가
실제로 거부했다. 한 trial에서는 pin 직렬화 수정과 local clone의 remote metadata 복원도
필요했다. 최종 실행은 둘 다 선택한 범위에서 통과했다. manifest quick mode의 내부 skip은
유지되므로 full product gate 통과를 뜻하지 않는다. 기존 기본 working copy는 보존했다.

held-out 작은 Go project는 이미 제공된 discovery에서 `go-test`를 선택해 실행했다.
해당 project를 위해 framework 코드를 추가 수정하지 않았고, 중앙 checkout 없이
runtime 실행과 standalone drift 검사를 통과했다.

| 관측 대상 | native 직접 실행 | 공통 runtime 전체 실행 |
| --- | --- | --- |
| 문서 gate | 0.78초 | 1.05초 |
| manifest quick gate | 4.37초 | 4.84초 |
| held-out Go test | 0.14초 | 0.54초 |

단일 warmed-cache 관측이며 wrapped 실행 뒤 직접 실행한 순서 효과가 있다. 속도 개선의
추정치가 아니다. 반복 업무 전체 시간, token 비용과 장기 유지보수 절감은 측정하지 않았다.
기존 runner를 직접 한 번 실행하던 업무에는 새 binding과 report 절차가 추가될 수 있다.
공통 결과 처리를 위한 새 소비자별 코드를 요구하지 않는다는 사실과 실제 수작업 감소는
서로 다른 결과다.

### 행동 평가와 결정

동일한 inherited model과 tool 한도·출력 한도에서 두 독립 평가자가 동일한 8개
증거 기반 완료 보고 사례를 처리했다. 기본 core와 core+신규 skill만 다르게 제공했다.
증거 불일치/skip/stale 5개와 충분한 증거가 있는 정상 사례 3개를 포함했다.
두 조건 모두 부족한 증거 5/5를 구분하고 정상 사례 3/3에서 불필요하게 범위를 넓히지
않았다. 신규 skill의 추가 개선은 관측되지 않았다.

한 쌍의 보고 과제 결과이며 실제 여러 단계 작업 수행, model 간 일반화, 장기 오류율이나
생산성 향상은 검증하지 않았다. 따라서 capability를 optional local candidate로 유지하고
portfolio 자동 도입이나 더 큰 workflow로 확장하지 않는다. 후속 시작 조건은 실제 반복
업무에서 수작업·재작업 감소가 관측되거나 명확한 추가 요구가 생기는 경우다.

public release, consumer 기본 working-copy adoption, full product/browser/live acceptance와
remote CI는 이번 범위 밖이다. private 평가 원문과 대상별 결과는 machine-local 계층에 두고
공개 artifact에는 정제된 판정·방법·한계만 남겼다. 역할이 끝난 spec과 active pointer는
정리하고 현재 상태와 후속 조건은 handoff/status/roadmap으로 이관했다.

## Operational workflows — local candidate

이전 검증 profile은 실행 결과를 공통화했지만 직접 실행 대비 수작업 감소나 agent 판단
개선을 입증하지 못했다. 후속 범위는 중복 갱신 검사를 제거하고 독립 변경의 배정·인계·통합을
실제 도구로 제공하는 것으로 정했다. 기존 core/native spec의 의미 판단 계약은 유지했다.

원래 완료 기준의 immutable 참조:
`2ba12c5a3e8979f07c3bfd7473e0447381c19ce7:docs/todo-operational-workflows/spec.md`.
기준을 결과에 맞춰 축소하지 않았다. 반복 수정 제거·실제 상태/실패 처리·standalone 실행과
동일 과제 비교를 대조했으며, 속도·비용 우위와 타 vendor 실행은 미입증으로 남겼다.

### 공통 갱신 검사

standalone checker가 선언·lock을 기준으로 generated header, output role, input, 공통 heading,
project/publication metadata와 profile 순서를 검사한다. 외부 source tag·서명 검증과 제품
고유 assertion/publication 호출은 기존 native gate가 계속 소유한다.

기존 소비 저장소 두 곳의 격리 clone에서 native script의 중복 공통 assertion을 각각 70줄,
61줄 제거했다. 한 번 연결한 뒤 다음 development version 갱신과 profile 제거를 실행했고
두 곳 모두 native script 수정 **0회**로 통과했다. native 필수 검사 파일을 없애면 standalone
정합성 검사는 성공하더라도 native gate는 실패했고, 복원 후 다시 성공했다. 이는 반복되는
공통 pin 수정 지점 제거의 evidence이며 전체 제품 gate나 portfolio adoption의 완료가 아니다.
최초 이관 스크립트의 구간 선택 오류 한 건은 shell 검사에서 검출해 수정한 뒤 다시 실행했다.

### 실제 파일 수정 비교

보고 문장 분류 대신 CSV loader와 정확한 decimal summary를 구현하는 동일한 두 파일 과제를
사용했다. SPEC과 8개 acceptance test를 실행 전에 고정하고, 동일한 source 자료·부모 모델과
설정을 상속한 Codex agent를 사용했다. 대조군은 직접 native 명령을 실행하는 단일 agent,
workflow 단일군은 전체 범위 assignment 하나, 다중군은 겹치지 않는 assignment 두 개다.
worker는 허용된 두 파일만 변경했고 frozen spec/test는 모든 결과에서 보존됐다.

각 arm의 총 도구 예산은 30으로 동일하게 제한했다. 단일 worker는 20, 다중 worker는 각각
10으로 두고 coordinator에 10을 남겼다. 관측 budget 단위는 worker 호출, coordinator의
init/assign/integrate, host dispatch와 최종 acceptance 감사다. 내부 subprocess 수와 token은
같은 단위가 아니며 전체 계측하지 않았다.

| 관측 | 기존 단일 | Workflow 단일 | Workflow 다중 |
| --- | --- | --- | --- |
| 고정 acceptance | 8/8 | 8/8 | 8/8 |
| worker 도구 호출 | 6 | 6 | 9 합계 |
| coordinator 작업 명령 | 0 | 3 | 4 |
| dispatch·최종 감사 포함 budget 사용 | 8/30 | 11/30 | 16/30 |
| worker 실행 구간 | 128.8초 | 98.2초 | 83.3초, 첫 시작부터 마지막 완료 |
| clone 배정 준비 | 공통 fixture 외 없음 | 0.93초 | 1.82초 |
| 별도 clone 통합·전체 검증 | 해당 없음 | 2.05초, 성공 | 2.34초, 성공 |
| 사람 개입 / 구현 재작업 | 0 / 0 | 0 / 0 | 0 / 0 |

workflow의 setup 시작부터 통합 종료까지 실제 경과는 각각 188.3초와 189.7초였다. 여기에는
coordinator의 배정·결과 수거 지연과 다른 검증 작업이 포함된다. worker 구간만으로 전체
작업이 빨라졌다고 주장하지 않는다. 다중군에서 packet 목록을 object로 가정한 읽기 오류
1회를 복구했으며 구현이나 acceptance를 변경하지 않았다. 최소 fixture의 일부 탐색 링크는
placeholder였고 세 arm 모두 고정 SPEC의 native 검사로 진행했다.

통합 결과에 독립적으로 같은 8개 acceptance를 다시 실행했고 범위와 frozen 자료를 대조했다.
workflow 두 군의 원본 source는 보존됐고 통합 실패는 없었다. 별도의 회귀 시험에서는 실제
native combined check 실패가 개별 worker PASS 이후에도 최종 실패로 남는 것을 검증했다.

이 비교는 작은 독립 파일 과제당 1회이며 무작위 반복이나 서비스 부하 통제가 없다. token과
금액은 미측정이다. 품질 우위·일반적인 속도 향상·비용 절감을 주장하지 않는다. 확인된 결과는
반복 native 수정 지점 제거, Codex worker의 실제 packet 실행, revision 인계와 별도 통합,
그리고 그 과정의 추가 호출 비용이다. 다른 vendor의 adapter 지원은 아직 미검증이다.

### 소유 artifact와 검증 한계

공통 checker/verification 연결은 `docs/VERIFICATION.md`, 명령·상태·재개·지원 경계는
`docs/WORK_COORDINATION.md`, compatibility는 `docs/COMPATIBILITY.md`가 소유한다.
`ai-first-verify` skill은 core의 일반 판단 예시 반복을 줄여 command와 결과 해석에 집중했다.

canonical local gate는 interface, verification, 실제 jj workspace, optional distribution과
기존 회귀 검증을 포함한다. CI는 checksum으로 고정한 jj 설치와 부재 시 실패를 연결했다.
이 결과는 local candidate이며 새 remote CI, release 또는 기본 소비 저장소 도입의 evidence가
아니다. 다음 확대는 실제 반복 과제에서 추가 호출 비용을 상쇄하는 운영 효과 또는 별도의
명시적 요구를 기준으로 판단한다.
