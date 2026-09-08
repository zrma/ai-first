# Open questions

결과를 바꾸는 미결정 사항은 없다.

- 의도의 source of truth는 기존 spec이다. 별도 intent 파일은 중복을 만든다.
- 공통 core는 변경 리뷰를 소유하고 PR 자동화와 native readiness는 소비 저장소가
  소유한다. 새 required field나 자동화 명령은 이번 범위에 포함하지 않는다.
- 완료 후 당시 spec을 확인해야 하면 immutable revision과 경로를 리뷰 기록에 남긴다.
  최신 계약은 이관된 artifact가 소유하며, 원본 packet 상시 보존은 요구하지 않는다.
