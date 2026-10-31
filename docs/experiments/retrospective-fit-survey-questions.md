# Retrospective Fit Survey: Questionnaire

> Experiment 2.5. The plan and the rules for reading the results are in [retrospective-fit-survey.md](retrospective-fit-survey.md).
>
> **The exact wording lives in [`examples/survey_forms.gs`](../../examples/survey_forms.gs)**, which creates the Google Forms. This page is a readable copy generated from that file. The IDs in backticks are column names for the analysis script and are not shown to respondents.

[English](#english) · [한국어](#한국어)

---

## English

### Intro (first screen)

**How well does work fit the way you live?** (about 10 minutes)

This survey is part of continuum-protocol, an open-source project that asks whether jobs fit people's rhythms of living, not just their skills.

- Anonymous. We don't ask for your name, email, employer, or job title.
- About 10 minutes. You can stop at any point. Nothing is saved until you submit.
- Only summary results are published. Individual answers are never posted.
- If you might want your answer deleted later, choose a code word at the end.
- Who can take part: you're 18 or older and have worked at least one job (part-time and freelance count) for 3 months or more.

### Consent

| # | ID | Question | Answer |
|---|----|------|------|
| 1 | `consent` | I've read the above and agree to take part. *(required)* | I agree |

### Part 1. You

Think about how you work best when nothing forces you otherwise.

| # | ID | Question | Answer |
|---|----|------|------|
| 2 | `self_energy` | When do you focus best? *(required)* | Morning / Afternoon / Evening or night / It varies across the day |
| 3 | `self_flex` | What kind of schedule suits you? *(required)* | 0 = Fixed, set hours … 10 = Choosing my own hours |
| 4 | `self_people` | How much working with others suits you? *(required)* | 0 = Mostly alone … 10 = Constant collaboration and meetings |
| 5 | `self_change` | How much change suits you? *(required)* | 0 = A stable, predictable routine … 10 = Frequent change and surprises |
| 6 | `self_pace` | What pace suits you? *(required)* | 0 = Steady and even … 10 = Intense sprints, then rest |

### Part 2. A job

Think of your current job, or the most recent one you did for at least 3 months. Describe how it actually ran day to day, not how it was advertised.

| # | ID | Question | Answer |
|---|----|------|------|
| 7 | `a_energy` | When did the work demand the most from you? *(required)* | Morning / Afternoon / Evening or night / Spread across the day |
| 8 | `a_flex` | How flexible was the schedule? *(required)* | 0 = Fixed hours … 10 = Fully flexible |
| 9 | `a_people` | How much did you work with others? *(required)* | 0 = Mostly alone … 10 = Constant collaboration and meetings |
| 10 | `a_change` | How much did things change? *(required)* | 0 = A stable routine … 10 = Frequent change and surprises |
| 11 | `a_pace` | What was the pace? *(required)* | 0 = Steady and even … 10 = Intense sprints |
| 12 | `a_fit` | Overall, how well did this job fit the way you live? *(required)* | 1 = Not at all … 7 = Very well |
| 13 | `a_adjust` | How much did you have to adjust yourself to keep up with this job? *(required)* | 0 = Not at all … 10 = Constantly |
| 14 | `a_check` | To show you're reading carefully, please choose 4 here. *(required)* | 1 … 7 |
| 15 | `a_current` | Are you still in this job? *(required)* | Yes / No |
| 16 | `a_duration` | How long have you been (or were you) in it? *(required)* | 3–6 months / 6–12 months / 1–3 years / Over 3 years |
| 17 | `a_note` | (Optional) In a sentence or two: what made it fit, or not fit? | Free text |
| 18 | `b_opt_in` | Could you also describe one other job that felt clearly different? (about 2 minutes) *(required)* | Yes / No, skip this |

"Yes" goes on to Part 3; "No" skips to Part 4.

### Part 3. A job that felt different

If the first job didn't fit you well, think of one that fit better. If it fit well, think of one that fit worse. Any job you did for at least 3 months counts.

| # | ID | Question | Answer |
|---|----|------|------|
| 19 | `b_energy` | [Second job] When did the work demand the most from you? *(required)* | Morning / Afternoon / Evening or night / Spread across the day |
| 20 | `b_flex` | [Second job] How flexible was the schedule? *(required)* | 0 = Fixed hours … 10 = Fully flexible |
| 21 | `b_people` | [Second job] How much did you work with others? *(required)* | 0 = Mostly alone … 10 = Constant collaboration and meetings |
| 22 | `b_change` | [Second job] How much did things change? *(required)* | 0 = A stable routine … 10 = Frequent change and surprises |
| 23 | `b_pace` | [Second job] What was the pace? *(required)* | 0 = Steady and even … 10 = Intense sprints |
| 24 | `b_fit` | [Second job] Overall, how well did this job fit the way you live? *(required)* | 1 = Not at all … 7 = Very well |
| 25 | `b_adjust` | [Second job] How much did you have to adjust yourself to keep up with this job? *(required)* | 0 = Not at all … 10 = Constantly |
| 26 | `b_current` | [Second job] Are you still in this job? *(required)* | Yes / No |
| 27 | `b_duration` | [Second job] How long have you been (or were you) in it? *(required)* | 3–6 months / 6–12 months / 1–3 years / Over 3 years |
| 28 | `b_note` | [Second job] (Optional) In a sentence or two: what made it fit, or not fit? | Free text |

### Part 4. Last questions (optional)

| # | ID | Question | Answer |
|---|----|------|------|
| 29 | `work_type` | Which is closest to the work you described? *(optional)* | Office or knowledge work / Creative work / Hands-on or service work / Care, health, or education / Other |
| 30 | `region` | Where do you mainly work? *(optional)* | Korea / Outside Korea |
| 31 | `source` | Where did you find this survey? *(optional)* | A friend sent it to me / A post or link someone shared / An online community / GitHub / SurveyCircle / Reddit / Other |
| 32 | `code_word` | (Optional) If you might want your answer deleted later, write a code word only you would know. | Free text |

### Closing message

Thank you for taking part. Summary results will be posted at github.com/DevAaronJeong/continuum-protocol. To delete your answer, enter your code word in this form: *(deletion form link, added by the script)*

---

## 한국어

### 안내 (첫 화면)

**지금 하는 일, 내 생활 방식과 잘 맞나요?** (약 10분)

이 설문은 오픈소스 프로젝트 continuum-protocol의 일부입니다. 이 프로젝트는 일이 사람의 능력뿐 아니라 생활의 리듬과도 맞는지를 탐구합니다.

- 익명입니다. 이름, 이메일, 회사명, 직함은 묻지 않습니다.
- 약 10분 걸립니다. 언제든 그만둘 수 있고, 제출하기 전에는 아무것도 저장되지 않습니다.
- 요약 결과만 공개합니다. 개별 응답은 공개하지 않습니다.
- 나중에 응답을 지우고 싶을 수도 있다면, 마지막에 나만 아는 암호 단어를 정해 두세요.
- 참여 대상: 만 18세 이상이고, 한 가지 이상의 일(아르바이트·프리랜서 포함)을 3개월 이상 해 본 분.

### 동의

| # | ID | 질문 | 답 |
|---|----|------|------|
| 1 | `consent` | 위 내용을 읽었고, 참여에 동의합니다. *(필수)* | 동의합니다 |

### 1부. 나

아무것도 강요받지 않을 때, 나는 어떻게 일할 때 가장 잘 되는지 떠올려 주세요.

| # | ID | 질문 | 답 |
|---|----|------|------|
| 2 | `self_energy` | 언제 가장 집중이 잘 되나요? *(필수)* | 오전 / 오후 / 저녁·밤 / 하루 중 그때그때 다름 |
| 3 | `self_flex` | 어떤 일정이 나에게 맞나요? *(필수)* | 0 = 정해진 시간에 일하기 … 10 = 내가 시간을 정하기 |
| 4 | `self_people` | 다른 사람과 얼마나 함께 일하는 게 맞나요? *(필수)* | 0 = 주로 혼자 … 10 = 끊임없는 협업과 회의 |
| 5 | `self_change` | 변화는 어느 정도가 맞나요? *(필수)* | 0 = 안정적이고 예측 가능한 루틴 … 10 = 잦은 변화와 돌발 상황 |
| 6 | `self_pace` | 어떤 속도가 맞나요? *(필수)* | 0 = 꾸준하고 고른 속도 … 10 = 강하게 몰아치고 쉬기 |

### 2부. 일 하나

지금 하고 있는 일, 또는 가장 최근에 3개월 이상 했던 일을 떠올려 주세요. 채용 공고에 적힌 모습이 아니라, 실제로 하루하루 어떻게 돌아갔는지를 기준으로 답해 주세요.

| # | ID | 질문 | 답 |
|---|----|------|------|
| 7 | `a_energy` | 그 일은 언제 가장 많은 것을 요구했나요? *(필수)* | 오전 / 오후 / 저녁·밤 / 하루 전체에 퍼져 있음 |
| 8 | `a_flex` | 일정은 얼마나 유연했나요? *(필수)* | 0 = 정해진 시간 … 10 = 완전히 자유 |
| 9 | `a_people` | 다른 사람과 얼마나 함께 일했나요? *(필수)* | 0 = 주로 혼자 … 10 = 끊임없는 협업과 회의 |
| 10 | `a_change` | 일이 얼마나 자주 바뀌었나요? *(필수)* | 0 = 안정적인 루틴 … 10 = 잦은 변화와 돌발 상황 |
| 11 | `a_pace` | 일의 속도는 어땠나요? *(필수)* | 0 = 꾸준하고 고름 … 10 = 강하게 몰아침 |
| 12 | `a_fit` | 전체적으로, 이 일은 내 생활 방식과 얼마나 잘 맞았나요? *(필수)* | 1 = 전혀 안 맞음 … 7 = 아주 잘 맞음 |
| 13 | `a_adjust` | 이 일을 따라가려고 나를 얼마나 맞춰야 했나요? *(필수)* | 0 = 전혀 … 10 = 늘 |
| 14 | `a_check` | 꼼꼼히 읽고 계신지 확인하는 문항입니다. 여기서는 4를 골라 주세요. *(필수)* | 1 … 7 |
| 15 | `a_current` | 지금도 이 일을 하고 있나요? *(필수)* | 예 / 아니요 |
| 16 | `a_duration` | 이 일을 얼마나 했나요(하고 있나요)? *(필수)* | 3~6개월 / 6~12개월 / 1~3년 / 3년 이상 |
| 17 | `a_note` | (선택) 무엇 때문에 잘 맞았는지, 혹은 안 맞았는지 한두 문장으로 적어 주세요. | 자유 응답 |
| 18 | `b_opt_in` | 느낌이 확실히 달랐던 다른 일도 하나 답해 주실 수 있나요? (약 2분) *(필수)* | 예 / 아니요, 건너뛸게요 |

"예"를 고르면 3부로, "아니요"를 고르면 4부로 넘어갑니다.

### 3부. 느낌이 달랐던 다른 일

첫 번째 일이 잘 안 맞았다면 상대적으로 잘 맞았던 일을, 잘 맞았다면 덜 맞았던 일을 떠올려 주세요. 3개월 이상 했던 일이면 됩니다.

| # | ID | 질문 | 답 |
|---|----|------|------|
| 19 | `b_energy` | [두 번째 일] 그 일은 언제 가장 많은 것을 요구했나요? *(필수)* | 오전 / 오후 / 저녁·밤 / 하루 전체에 퍼져 있음 |
| 20 | `b_flex` | [두 번째 일] 일정은 얼마나 유연했나요? *(필수)* | 0 = 정해진 시간 … 10 = 완전히 자유 |
| 21 | `b_people` | [두 번째 일] 다른 사람과 얼마나 함께 일했나요? *(필수)* | 0 = 주로 혼자 … 10 = 끊임없는 협업과 회의 |
| 22 | `b_change` | [두 번째 일] 일이 얼마나 자주 바뀌었나요? *(필수)* | 0 = 안정적인 루틴 … 10 = 잦은 변화와 돌발 상황 |
| 23 | `b_pace` | [두 번째 일] 일의 속도는 어땠나요? *(필수)* | 0 = 꾸준하고 고름 … 10 = 강하게 몰아침 |
| 24 | `b_fit` | [두 번째 일] 전체적으로, 이 일은 내 생활 방식과 얼마나 잘 맞았나요? *(필수)* | 1 = 전혀 안 맞음 … 7 = 아주 잘 맞음 |
| 25 | `b_adjust` | [두 번째 일] 이 일을 따라가려고 나를 얼마나 맞춰야 했나요? *(필수)* | 0 = 전혀 … 10 = 늘 |
| 26 | `b_current` | [두 번째 일] 지금도 이 일을 하고 있나요? *(필수)* | 예 / 아니요 |
| 27 | `b_duration` | [두 번째 일] 이 일을 얼마나 했나요(하고 있나요)? *(필수)* | 3~6개월 / 6~12개월 / 1~3년 / 3년 이상 |
| 28 | `b_note` | [두 번째 일] (선택) 무엇 때문에 잘 맞았는지, 혹은 안 맞았는지 한두 문장으로 적어 주세요. | 자유 응답 |

### 4부. 마지막 질문 (선택)

| # | ID | 질문 | 답 |
|---|----|------|------|
| 29 | `work_type` | 답한 일과 가장 가까운 것은? *(선택)* | 사무·지식 노동 / 창작 / 현장·서비스 / 돌봄·보건·교육 / 기타 |
| 30 | `region` | 주로 어디서 일하나요? *(선택)* | 한국 / 한국 밖 |
| 31 | `source` | 이 설문을 어디서 보셨나요? *(선택)* | 지인이 직접 보내줌 / 지인이 공유한 글이나 링크 / 온라인 커뮤니티 / GitHub / SurveyCircle / Reddit / 기타 |
| 32 | `code_word` | (선택) 나중에 응답 삭제를 원할 수도 있다면, 나만 아는 암호 단어를 적어 주세요. | 자유 응답 |

### 마무리 문구

참여해 주셔서 고맙습니다. 요약 결과는 github.com/DevAaronJeong/continuum-protocol 에 올라갑니다. 응답 삭제를 원하면 이 양식에 암호 단어를 입력해 주세요: *(삭제 양식 링크, 스크립트가 자동으로 넣음)*
