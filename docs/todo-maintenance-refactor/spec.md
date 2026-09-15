# 문서 탐색과 렌더러 유지보수 정리

상태: 진행 중

## 문제와 원하는 결과

현재 상태와 roadmap에 완료 이력이 중복되어 현재 작업을 찾고 release 결과를 갱신할
지점이 늘었다. 렌더러 build는 문서 합성, optional output 보호, binding 검사와 lock
생성을 함께 처리하고 결정성 테스트도 지침 전달·독립 실행까지 한 번에 검사한다.
현재·이력 문서의 소유를 명확히 하고 렌더러와 테스트의 변경·실패 원인을 좁힌다.

## 범위와 영향

1. status·roadmap·handoff의 역할 정리와 완료 지식 보존.
2. render 모듈 내부의 문서 합성, optional output 구성, binding 검사와 lock 생성 분리.
3. 기존 테스트를 결정성·지침 전달·독립 실행 등 검증 목적별로 분리.

영향 대상은 framework 유지보수자와 renderer를 사용하는 소비 저장소다.
두 logical local change로 마감한다. 첫 change는 문서 정리와 이 구현 기준을 보존하고,
두 번째 change는 구현·검증 결과 이관 후 packet과 active pointer를 제거한다.

## 유지할 조건과 non-goal

CLI·선언/lock schema·profile 순서·generated 문서와 runtime·source pin 검증을 유지한다.
충돌·symlink escape·기존 미소유/수정 파일 보호·opt-out 보존 동작을 유지한다.
framework source digest의 변경은 예상되지만 그 밖의 합성 결과 차이는 허용하지 않는다.
새 모듈 배포 체계, 중앙/standalone checker 통합, verification·coordination 재설계,
지침 내용 변경, 성능 최적화, release·push·소비 adoption은 범위 밖이다.

## Acceptance와 검증

- 현재 상태 문서에서 중복 완료 목록을 제거하고 고유 결과·판단·한계를 이관한다.
- build에서 합성·optional output·binding·lock 단계를 명확히 구별한다.
- 변경 전 renderer와 같은 입력의 문서·runtime·lock 결과를 대조한다.
  동일 framework source를 주어 source digest 차이와 로직 차이를 구별한다.
- 기존 지침 전달 assertion과 실패/보호 시나리오는 삭제·완화하지 않는다.
- 연결된 native gate로 generated/standalone/interface, publication, navigation,
  CI contract와 전체 회귀 검증을 실행한다. 실제 jj 통합 skip을 확인한다.
- 구조·판단 이유는 architecture, 검증 범위·한계는 완료 요약에 이관한다.
  원래 spec을 첫 local change로 참조하고 stale pointer와 packet을 정리한다.

실제 소비 저장소·remote CI·live 동작과 성능·token 절감은 이번 검증 범위 밖이다.
