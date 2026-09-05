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


## Spec-to-artifact lifecycle — local framework

`1.5.0-dev` core에 milestone/bounded specification의 설계 정립, 구현 중 정합성,
완료 지식 이관과 작업 문서 정리 계약을 반영했다. 원본 보존은 명시적인 추적·운영
필요가 있을 때만 선택하며 자동 폴더 이동으로 완료를 대신하지 않는다.

기존 완료 packet의 설계 선택은 `docs/ARCHITECTURE.md`, 후속 capability 조건은
`docs/COMPATIBILITY.md`, 운영 lifecycle은 `docs/WORK_LIFECYCLE.md`로 이관했다.
과거 결과와 검증 범위는 이 문서에 유지하고 원본 spec·질문 파일은 정리했다.

검증: `scripts/check.sh`, central/standalone drift, publication/interface gate와
24개 unit fixture. archive 없는 완료 artifact, stale reference, spec 없는 질문 파일을
검증했다. 이 결과는 지침의 구조·합성과 문서 정합성 검증이며 model 행동의 실측
평가나 새 release 및 소비 저장소 publication 완료를 의미하지 않는다.

## Spec-to-artifact lifecycle — consumer preparation

현재 원격 기본 브랜치의 관리 의도와 비아카이브 상태를 확인한 소비 저장소를
기본 working copy 밖의 colocated jj checkout에서 준비했다. immutable candidate
pin, generated artifact와 repository-native interface의 source identity를 함께 갱신했다.

공통 계약과 이미 일치하는 native todo 정리 절차는 보존했다. checklist 중심의
설명은 spec 정립과 artifact 이관 기준으로 보충했고 bootstrap 길이 제한은 상세
정책의 소유 문서로 안내하는 방식으로 유지했다.

검증: 소비 저장소별 standalone/interface 및 repository-native gate 통과. native
절차가 요구하는 작업 packet은 검증 뒤 지식을 이관하고 정리했다. 대상별 명령과
판정은 machine-local coordination에서 관리한다. optional runtime acceptance와
live 배포, 최종 release pin 및 remote/same-SHA CI는 이 후보 검증에 포함하지 않았다.
