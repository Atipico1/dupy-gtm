# GTM 자료 안내

## 공개 문서

- [진행 기록](progress.md)
- [7단계 루프](dupy-gtm-loop.md)
- [실행 기본 설정](config.json)
- [운영 스킬](../.agents/skills/dupy-gtm-loop/SKILL.md)
- [레퍼런스·편집 계약](reference-editing.md)
- [예약·게시 계약](publishing.md)
- [실행 기록 계약](run-records.md)
- [설계 당시 검수](skill-dry-run-review.md)
- [Harness² 연구 메모](../research/harness2-analysis.md)
- [제품 근거](../research/dupy-product-sot.md)

## 비공개 로컬 자료

원본 촬영물·선택한 인물·음성 프로필은 `assets/`, 제작 작업은 `creative/`, 내보내기는 `outputs/`, 실행별 결과와 영수증은 `runs/`에 둔다. 채널·상세 모델 설정은 `workflow/config.local.json`에서 관리한다. 이 자료는 Git에 포함되지 않으며 새 clone에는 없다.

각 회차의 `run.json`, 단계 기록, 편집 타임라인과 검수 기록으로 원본부터 최종 선택본을 추적한다. 사람에게 결과물을 전달할 때에는 공개 저장소에 올리는 대신 해당 사용자가 열 수 있는 절대 파일 경로나 승인된 전달 위치를 사용한다. 이전 파일을 덮어쓰거나 실패한 결과를 완료본으로 표시하지 않는다.
