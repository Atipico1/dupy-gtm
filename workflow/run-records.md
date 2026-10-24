# 실행별 JSON 기록과 부분 실행

Dupy GTM의 전체 실행, 개별 단계/스킬, 재실행, 개선 작업마다 `scripts/run_artifacts.py start`로 새 폴더를 만든다. 폴더 이름은 KST 시각(마이크로초)+랜덤8자리다. 예: `20261024T180000123456+0900-a1b2c3d4`. 시간은 정렬·추적용이며 암호학적 해시라고 부르지 않는다. 뒤의 난수는 동시 실행 충돌 방지용이다.

```text
runs/<run_id>/
  run.json                         요청·선택 단계·실행 범위·이전 실행·설정/스킬 스냅샷
  stages/03-planning/<record>.json  각 시도별 기록, 기존 기록을 덮어쓰지 않음
  stages/04-plan-review/<record>.json
  artifacts/                       해당 실행의 기획·음성·영상·미리보기 등
```

## 부분 실행

사용자 요청에서 `selected_stages`와 `scope`를 먼저 정한다. 단계는 아래에서 고른다.

| ID | 역할 |
|---|---|
| 01-performance | 자기 성과 분석 |
| 02-references | 시장·레퍼런스 분석 |
| 03-planning | 기획 |
| 04-plan-review | 기획 리뷰 |
| 05-production | 콘텐츠 제작(음성만/영상만/조립만도 scope로 제한) |
| 06-content-review | 콘텐츠 리뷰 |
| 07-publishing | 게시 |
| 08-improvement | 별도 워크플로우 개선 |
| maintenance | 스킬·설정 정비 |

- “기획만”: 03. 기존 제품/레퍼런스 근거를 입력으로 선택한다. 새 시장 수집·제작을 자동 실행하지 않는다.
- “조사하고 기획 리뷰까지”: 02·03·04. 자기 계정 분석은 별도 요구나 필요 근거가 없다면 포함하지 않는다.
- “이 대사 음성만”: 05, scope=audio_only. 선택된 음성 프로필과 대사만 필요하다. 인물/배경 사진·완성 영상 기획을 불필요한 필수조건으로 삼지 않는다. 영상·게시 제외.
- “이 영상 리뷰만”: 06. 기존 파일과 해당 기획/제품 근거를 연결한다.
- “통과한 버전 게시”: 07. 기존 PASS 기록의 정확한 파일·문안·계정과 현재 파일 해시가 일치해야 한다. 리뷰가 없거나 변경됐으면 게시하지 않고 필요한 리뷰를 알린다.
- “이번 실행 보고 루프 개선”: 08. 원본 실행을 연결하고 개선 실험 산출물도 이번 실행 artifacts 아래에 둔다.

선행 입력은 기존 실행의 파일/기록/해시로 재사용할 수 있다. 요청 범위 밖 단계는 자동 추가하지 않는다. 필수 입력이 없으면 가능한 독립 작업을 진행하고 해당 단계는 blocked로 남긴다. 실행 중 중지·범위 축소는 즉시 우선한다. 선택 안 된 단계는 성공으로 표시하지 않는다.

기존 실행을 이어가는 새 사용자 요청도 새 run_id를 만들고 `source_runs`로 연결한다. 같은 요청 안의 재시도/리뷰 회귀는 같은 실행 아래 새 단계 기록으로 남긴다. 승인된 범위의 회귀만 허용한다. 실제 실행 승인은 기존 workflow activation 계약을 따르며 기록 도구 자체가 제작·게시를 승인하거나 실행하지 않는다.

## 단계 JSON 계약

내부 사고과정 원문이 아니라 **검토 가능한 판단 근거 요약**을 기록한다. 사용한 입력, 관측, 비교한 선택지와 채택 이유, 수정 전후, 결론과 근거를 사람이 재검토할 수 있어야 한다. 수행하지 않은 검증·고민을 꾸며서 채우지 않는다.

```json
{
  "status": "completed",
  "skill": "dupy-gtm-loop",
  "inputs": [{"uri": "file:///absolute/source.json", "sha256": "actual-file-hash", "purpose": "레퍼런스 근거", "source_run_id": null}],
  "observations": [{"summary": "실제로 확인한 사실", "evidence_uri": "file:///absolute/evidence.json"}],
  "decision_summary": "검토한 대안과 채택 이유를 짧게 설명",
  "revisions": [{"before": "기존 판단 또는 결과", "trigger": "수정 원인과 근거", "after": "수정 결과"}],
  "conclusion": "최종 결정 및 한계",
  "outputs": [{"uri": "file:///absolute/result.json", "sha256": "actual-file-hash", "kind": "plan"}],
  "checks": [{"name": "사실 확인", "result": "passed", "evidence_uri": "file:///absolute/check.json"}],
  "error": null,
  "next_action": "선택 범위 안의 다음 단계 또는 종료"
}
```

배열은 해당 사항 없으면 빈 배열. 로컬 입력/출력에는 가능하면 실제 SHA-256, 원격 자료에는 수집시각과 출처 URL을 기록한다. 수치/판단의 불확실성도 결론에 남긴다. 실패·중지·응답 불명도 기록한다. 비밀키·쿠키·인증코드·음성 base64·서명된 일회성 URL을 넣지 않는다. 원시 데이터 전체를 중복 복사하기보다 안전한 로컬 파일을 가리킨다.

기록 상태: completed / needs_revision / blocked / failed / unknown / cancelled. 리뷰 결과는 checks와 conclusion에 PASS/REVISE/UNKNOWN을 명시한다. 단계 출력 뒤 기록을 저장하고 다음 단계로 간다. 중단 시 마지막으로 확인한 상태까지 남긴다. 유료 생성·게시 전 요청 의도/입력 해시와 pending 상태를 별도 작업 영수증으로 먼저 저장해, 응답 유실 시 중복 실행을 막는다.

## 실행 예

```sh
python3 scripts/run_artifacts.py start --request '기존 레퍼런스로 기획하고 리뷰만' --stages 03-planning 04-plan-review --scope planning_only
python3 scripts/run_artifacts.py record --run /absolute/runs/RUN_ID --stage 03-planning --input /absolute/stage-result.json
```

record 입력 JSON도 해당 run의 artifacts 안에 둔다. 각 저장은 원자적이며 기존 기록을 교체하지 않는다. 병렬 작업자는 자기 단계 기록 파일만 쓰고 오케스트레이터가 상태·선정 결과를 관리한다. 완료 답변에서 실행 폴더와 주요 산출물을 링크한다. `runs/`는 로컬 보존하며 Git 제외를 유지한다. 이 도구는 JSON 형식과 단계 범위를 검증하지만, 근거의 진위나 게시 권한을 자동 판정하지 않는다.
