# Dupy GTM

- 먼저 `README.md`, `workflow/config.json`, `workflow/dupy-gtm-loop.md`를 읽는다. 제품 주장은 `research/dupy-product-sot.md`와 실제 근거를 대조한다.
- 운영 진입점은 `.agents/skills/dupy-gtm-loop/SKILL.md`다. 지정 레퍼런스의 훅·사용 장면·CTA를 변주하고 원본 URL과 근거를 남긴다.
- 자기 계정 성과는 연결된 인앱 브라우저, 소셜 레퍼런스는 글로벌 `tikhub` CLI를 사용한다. 기존 자료와48시간 캐시를 우선하며 응답 payload를 확인한다.
- 설계 요청은 생성·게시 실행이 아니다. 현재 사용자 지시와 회차 활성화 범위를 확인하고, 중지 요청을 최우선으로 따른다.
- 제작은 영상 생성 모델와 음성 생성 모델 사용한다. 음성은 `assets/voices/dupy-female-v1/profile.json`의 denoise 참고 WAV·해시·전사를 고정 재사용한다. 전용 인물·배경·예산을 확인하고 모델을 임의 교체하지 않는다.
- 제작과 리뷰를 분리한다. 최종 영상·음성·문안·CTA·계정을 검수하고, 파일 변경 시 이전 PASS를 무효화한다. 불명확한 생성·게시 응답은 조회로 복구하며 중복 전송하지 않는다.
- 별도 개선 역할은 기존/수정 절차를 같은 자료로 비교한다. 검증된 변경만 다음 회차에 적용하고 실행 중 규칙은 고정한다.
- 미디어·원시 응답·자격증명은 커밋하지 않는다. `.gitignore`를 지키고 다른 작업의 로컬 파일을 삭제하지 않는다. 문서/스킬 변경 후 링크·설정·스킬 형식을 검증한다.
- 매 실행은 `workflow/run-records.md`에 따라 시간 기반 새 폴더와 단계별 JSON을 남긴다. 사용자 요청 단계만 실행하며 입력·근거 요약·수정·결론·산출물·오류를 기록하고 이전 시도를 덮어쓰지 않는다.
- assets/·creative/·outputs/·runs/는 비공개 로컬 자료다. Git에 강제 추가하거나 공개 호스팅하지 않는다. 생성 서비스 입력도 현재 승인된 제작 범위에 한정한다. 레퍼런스의 화면/컷/자막/내용/훅·CTA와 편집 규칙은 workflow/reference-editing.md를 따른다.
- 실제 레퍼런스 채널 핸들은 비공개 workflow/config.local.json에 있다. 있으면 config.json보다 우선한다.
