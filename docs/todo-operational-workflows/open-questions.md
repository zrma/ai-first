# Open questions

blocking question은 없다.

- 공통 interface의 source of truth는 pinned declaration과 generated lock이다. 독립적인
  upstream tag·signature 검증은 기존 publication/source gate가 담당한다.
- 작업 배정 범위는 최초 버전에서 파일/디렉터리 단위의 독립 작업으로 제한한다. 같은
  경로에 순서 의존성이 있으면 coordinator가 순차 작업으로 분리한다.
- runtime adapter는 기존 host의 agent 호출을 사용하고 CLI는 VCS·인계·통합 상태를
  소유한다. 외부 API key나 새로운 유료 서비스를 요구하지 않는다.
