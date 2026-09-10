---
name: ai-first-verify
description: 변경을 검증하거나 완료를 보고할 때 연결된 native 검증을 실행하고 요청 시나리오와 증거를 대조한다. ai-first verification profile이 설치된 저장소에 사용하며 일반 질의나 계획만 요청한 경우 검증 실행으로 확대하지 않는다.
---

# Change verification

사용자가 원한 결과와 실제 검증 범위를 연결한다. 공통 runtime은 실행 결과를 처리하고,
repository의 native runner와 acceptance 자료는 제품별 판단 근거를 제공한다.

1. 원래 요청·기존 spec에서 성공 조건을 확인한다. 관찰 대상, 실행 경로, 방향과 환경이
   결과 해석을 바꿀 때만 이를 구체화한다. 예를 들어 새 브라우저 탭에서의 성공은 기존
   탭 복구를, outbound 연결은 inbound 수신을, version pin 변경은 실제 migration을
   입증하지 않는다. 필요한 증거가 이미 있으면 같은 검사를 반복하지 않는다.
2. 저장소 루트에서 `python3 .ai-first/verify.py --plan`을 실행한다. binding이 없으면
   후보 명령과 native 문서를 읽어 대상·side effect·현재 권한을 확인하고 `--bind ID`로
   선택한다. 후보가 없으면 기존 native entrypoint 하나를 binding으로 연결한다.
   내부 명령 목록이나 공통 실행 wrapper를 새로 만들지 않는다. binding 수정 뒤에는
   pinned framework의 render로 lock을 갱신한다. 기존 binding도 현재 요청보다 넓으면
   `--select ID`로 범위를 줄인다. 미선택 check는 not_run으로 남는 것이 정상이다.
3. 현재 요청이 허용한 범위에서 `python3 .ai-first/verify.py --run`을 실행한다.
   결과를 보존해야 하면 `--output <private-report>`로 repository 외부의 새 파일을
   지정한다. JSON의 raw stderr 분리나 private 저장은 publication 승인을 대신하지 않는다.
4. 결과와 native 출력의 실제 test count·skip·scope를 확인한다. native runner가 내부
   skip을 exit 0으로 숨기면 공통 runtime의 passed만으로 전체 검증을 주장하지 않는다.
   재사용하는 결과는 `--report <private-report>`로 freshness를 확인한다. 소스 identity는
   ignored dependency, 외부 상태나 실행 환경 동일성을 보증하지 않는다.
5. 요청의 성공 조건마다 현재 증거가 충분한지 판단한다. runner가 다루지 않는 제품
   시나리오는 기존 browser/live/artifact 검사로 필요한 만큼만 보완한다. 증거가 없으면
   미검증으로 남기며 기능 미충족과 구분한다. 검증 지표를 인간의 시각적·제품 판단으로
   대체하지 않는다. 완료 보고에는 결과, 의미 있는 검증, 남은 한계를 간결하게 연결한다.

## Binding

`.ai-first/verification.toml`은 아래와 같은 작은 adapter다. `argv`는 shell 문자열이
아닌 argument 배열이며 저장소 루트에서 실행된다. 기본 timeout은 300초다.
기존 native 모드·선택 옵션은 해당 runner의 계약을 따른다.

```toml
schema_version = 1

[[checks]]
id = "native-check"
argv = ["sh", "scripts/check.sh"]
coverage = ["Repository native local gate"]
timeout_seconds = 300
skip_exit_codes = [77]
```

skip exit code는 runner가 실제 정의한 경우에만 지정한다. 없는 것을 추정하지 않는다.
runtime은 passed, failed, skipped, unavailable, timeout, interrupted와 not_run을
구분한다. 하나라도 passed가 아니면 전체 결과는 incomplete이며, source 변경은 stale이다.
완료 조건의 의미, external write 권한, human acceptance와 lifecycle closeout은 기존
repository 계약이 소유한다.
