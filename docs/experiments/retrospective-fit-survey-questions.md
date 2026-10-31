# Retrospective Fit Survey: Questionnaire

> Experiment 2.5. The plan and the rules for reading the results are in [retrospective-fit-survey.md](retrospective-fit-survey.md).
>
> Each question has an ID in backticks (for example `self_energy`). The IDs are column names for the analysis script. Don't show them to respondents.

[English](#english) · [한국어](#한국어) · [Setting up the form](#setting-up-the-form)

---

## English

### Intro (shown before the first question)

**How well does work fit the way you live?** (about 10 minutes)

This survey is part of continuum-protocol, an open-source project that asks whether jobs fit people's rhythms of living, not just their skills.

- **Anonymous.** We don't ask for your name, email, employer, or job title.
- **About 10 minutes.** You can stop at any point. Nothing is saved until you submit.
- **Only summary results are published.** Individual answers are never posted.
- **Deletion.** If you might want your answer deleted later, choose a code word at the end.
- **Who can take part.** You're 18 or older and have worked at least one job (part-time and freelance count) for 3 months or more.

`consent` I've read the above and agree to take part. *(required)*

### Part 1. You

Think about how you work best when nothing forces you otherwise.

| # | ID | Question | Answer |
|---|----|----------|--------|
| 1 | `self_energy` | When do you focus best? | Morning / Afternoon / Evening or night / It varies across the day |
| 2 | `self_flex` | What kind of schedule suits you? | 0 = fixed, set hours … 10 = choosing my own hours |
| 3 | `self_people` | How much working with others suits you? | 0 = mostly alone … 10 = constant collaboration and meetings |
| 4 | `self_change` | How much change suits you? | 0 = a stable, predictable routine … 10 = frequent change and surprises |
| 5 | `self_pace` | What pace suits you? | 0 = steady and even … 10 = intense sprints, then rest |

### Part 2. A job *(required)*

Think of a job you have now or had, for at least 3 months. Describe how it actually ran day to day, not how it was advertised.

| # | ID | Question | Answer |
|---|----|----------|--------|
| 6 | `a_energy` | When did the work demand the most from you? | Morning / Afternoon / Evening or night / Spread across the day |
| 7 | `a_flex` | How flexible was the schedule? | 0 = fixed hours … 10 = fully flexible |
| 8 | `a_people` | How much did you work with others? | 0 = mostly alone … 10 = constant collaboration and meetings |
| 9 | `a_change` | How much did things change? | 0 = a stable routine … 10 = frequent change and surprises |
| 10 | `a_pace` | What was the pace? | 0 = steady and even … 10 = intense sprints |
| 11 | `a_fit` | Overall, how well did this job fit the way you live? | 1 = not at all … 7 = very well |
| 12 | `a_adjust` | How much did you have to adjust yourself to keep up with this job? | 0 = not at all … 10 = constantly |
| 13 | `a_check` | To show you're reading carefully, please choose 4 here. | 1 … 7 |
| 14 | `a_current` | Are you still in this job? | Yes / No |
| 15 | `a_duration` | How long have you been (or were you) in it? | 3–6 months / 6–12 months / 1–3 years / Over 3 years |
| 16 | `a_note` | *(optional)* In a sentence or two: what made it fit, or not fit? | Free text |

### Part 3. Another job *(optional)*

If you can, think of another job that felt different from the first one. Skip this part if you don't have one.

Same questions as 6–12 and 14–16, with IDs starting with `b_`:
`b_energy`, `b_flex`, `b_people`, `b_change`, `b_pace`, `b_fit`, `b_adjust`, `b_current`, `b_duration`, `b_note`

### Part 4. Last questions *(optional)*

| # | ID | Question | Answer |
|---|----|----------|--------|
| 27 | `work_type` | Which is closest to the work you described? | Office or knowledge work / Creative work / Hands-on or service work / Care, health, or education / Other |
| 28 | `region` | Where do you mainly work? | Korea / Outside Korea |
| 29 | `code_word` | If you might want your answer deleted later, write a code word only you would know. | Free text |

### Closing message

Thank you for taking part. Summary results will be posted at github.com/DevAaronJeong/continuum-protocol. To delete your answer, enter your code word in the deletion form: *(link)*

---

## 한국어

### 안내 (첫 질문 전에 표시)

**지금 하는 일, 내 생활 방식과 잘 맞나요?** (약 10분)

이 설문은 오픈소스 프로젝트 continuum-protocol의 일부입니다. 이 프로젝트는 일이 사람의 능력뿐 아니라 생활의 리듬과도 맞는지를 탐구합니다.

- **익명입니다.** 이름, 이메일, 회사명, 직함은 묻지 않습니다.
- **약 10분 걸립니다.** 언제든 그만둘 수 있고, 제출하기 전에는 아무것도 저장되지 않습니다.
- **요약 결과만 공개합니다.** 개별 응답은 공개하지 않습니다.
- **삭제 요청:** 나중에 응답을 지우고 싶을 수도 있다면, 마지막에 나만 아는 암호 단어를 정해 두세요.
- **참여 대상:** 만 18세 이상이고, 한 가지 이상의 일(아르바이트·프리랜서 포함)을 3개월 이상 해 본 분.

`consent` 위 내용을 읽었고, 참여에 동의합니다. *(필수)*

### 1부. 나

아무것도 강요받지 않을 때, 나는 어떻게 일할 때 가장 잘 되는지 떠올려 주세요.

| # | ID | 질문 | 답 |
|---|----|------|----|
| 1 | `self_energy` | 언제 가장 집중이 잘 되나요? | 오전 / 오후 / 저녁·밤 / 하루 중 그때그때 다름 |
| 2 | `self_flex` | 어떤 일정이 나에게 맞나요? | 0 = 정해진 시간에 일하기 … 10 = 내가 시간을 정하기 |
| 3 | `self_people` | 다른 사람과 얼마나 함께 일하는 게 맞나요? | 0 = 주로 혼자 … 10 = 끊임없는 협업과 회의 |
| 4 | `self_change` | 변화는 어느 정도가 맞나요? | 0 = 안정적이고 예측 가능한 루틴 … 10 = 잦은 변화와 돌발 상황 |
| 5 | `self_pace` | 어떤 속도가 맞나요? | 0 = 꾸준하고 고른 속도 … 10 = 강하게 몰아치고 쉬기 |

### 2부. 일 하나 *(필수)*

지금 하고 있거나 예전에 3개월 이상 했던 일 하나를 떠올려 주세요. 채용 공고에 적힌 모습이 아니라, 실제로 하루하루 어떻게 돌아갔는지를 기준으로 답해 주세요.

| # | ID | 질문 | 답 |
|---|----|------|----|
| 6 | `a_energy` | 그 일은 언제 가장 많은 것을 요구했나요? | 오전 / 오후 / 저녁·밤 / 하루 전체에 퍼져 있음 |
| 7 | `a_flex` | 일정은 얼마나 유연했나요? | 0 = 정해진 시간 … 10 = 완전히 자유 |
| 8 | `a_people` | 다른 사람과 얼마나 함께 일했나요? | 0 = 주로 혼자 … 10 = 끊임없는 협업과 회의 |
| 9 | `a_change` | 일이 얼마나 자주 바뀌었나요? | 0 = 안정적인 루틴 … 10 = 잦은 변화와 돌발 상황 |
| 10 | `a_pace` | 일의 속도는 어땠나요? | 0 = 꾸준하고 고름 … 10 = 강하게 몰아침 |
| 11 | `a_fit` | 전체적으로, 이 일은 내 생활 방식과 얼마나 잘 맞았나요? | 1 = 전혀 안 맞음 … 7 = 아주 잘 맞음 |
| 12 | `a_adjust` | 이 일을 따라가려고 나를 얼마나 맞춰야 했나요? | 0 = 전혀 … 10 = 늘 |
| 13 | `a_check` | 꼼꼼히 읽고 계신지 확인하는 문항입니다. 여기서는 4를 골라 주세요. | 1 … 7 |
| 14 | `a_current` | 지금도 이 일을 하고 있나요? | 예 / 아니요 |
| 15 | `a_duration` | 이 일을 얼마나 했나요(하고 있나요)? | 3~6개월 / 6~12개월 / 1~3년 / 3년 이상 |
| 16 | `a_note` | *(선택)* 무엇 때문에 잘 맞았는지, 혹은 안 맞았는지 한두 문장으로 적어 주세요. | 자유 응답 |

### 3부. 다른 일 하나 *(선택)*

가능하다면 첫 번째와 느낌이 달랐던 다른 일을 떠올려 주세요. 없으면 건너뛰어도 됩니다.

6–12번, 14–16번과 같은 질문이고, ID는 `b_`로 시작합니다:
`b_energy`, `b_flex`, `b_people`, `b_change`, `b_pace`, `b_fit`, `b_adjust`, `b_current`, `b_duration`, `b_note`

### 4부. 마지막 질문 *(선택)*

| # | ID | 질문 | 답 |
|---|----|------|----|
| 27 | `work_type` | 답한 일과 가장 가까운 것은? | 사무·지식 노동 / 창작 / 현장·서비스 / 돌봄·보건·교육 / 기타 |
| 28 | `region` | 주로 어디서 일하나요? | 한국 / 한국 밖 |
| 29 | `code_word` | 나중에 응답 삭제를 원할 수도 있다면, 나만 아는 암호 단어를 적어 주세요. | 자유 응답 |

### 마무리 문구

참여해 주셔서 고맙습니다. 요약 결과는 github.com/DevAaronJeong/continuum-protocol 에 올라갑니다. 응답 삭제를 원하면 삭제 요청 양식에 암호 단어를 입력해 주세요: *(링크)*

---

## Setting up the form

- **Scales:** use a linear scale for 0–10 and 1–7 questions, with the end labels above.
- **No identity:** don't collect emails, and turn off any setting that requires sign-in or records who answered.
- **Deletion form:** make a second, one-question form ("Delete my answer: code word") and put its link in the closing message.
- **Language:** run the Korean and English versions as two forms, or one form per language. The analysis script accepts answers in either language.
- **Before opening:** check that the plan ([retrospective-fit-survey.md](retrospective-fit-survey.md)) and the analysis script are committed. Neither may change after the survey opens.
