# Open questions

의존 구현을 막는 미결정은 없다.

- 기존 release pin과 native 절차를 보존하고 충돌하는 version assertion 또는 계약만
  저장소별로 수정한다. 새로운 필수 packet 형식을 일괄 도입하지 않는다.
- 갱신 중 remote가 바뀌면 새 기준에서 재검증하고 기존 작업을 덮어쓰지 않는다.
- 소비 저장소의 제품 release 또는 운영 환경 변경은 framework adoption에 포함하지 않는다.
