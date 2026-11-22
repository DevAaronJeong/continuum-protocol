/**
 * Experiment 2.5 - creates the survey forms in Google Forms.
 *
 * How to use:
 *   1. Go to https://script.google.com and click "New project".
 *   2. Delete the sample code, paste this whole file, and save.
 *   3. Choose the function "createSurveyForms" and click Run.
 *      Google asks for permission to create forms in your Drive. Allow it.
 *   4. Open View > Logs (or Execution log). It lists the links to the three forms:
 *      Korean survey, English survey, and the deletion-request form.
 *
 * This file is the single source of the question wording. The analysis script
 * (examples/survey_analysis.py) reads the QUESTIONS list below to recognise the
 * columns in the Google Forms CSV export, so keep the two in sync by editing
 * only this list.
 *
 * Plan and reading rules: docs/experiments/retrospective-fit-survey.md
 */

// BEGIN QUESTIONS (JSON: edited by hand, read by survey_analysis.py)
const QUESTIONS = [
  {"id": "consent", "page": "intro", "type": "consent", "required": true,
   "ko": "위 내용을 읽었고, 참여에 동의합니다.", "en": "I've read the above and agree to take part.",
   "ko_choices": ["동의합니다"], "en_choices": ["I agree"]},

  {"id": "self_energy", "page": "self", "type": "choice", "required": true,
   "ko": "언제 가장 집중이 잘 되나요?", "en": "When do you focus best?",
   "ko_choices": ["오전", "오후", "저녁·밤", "하루 중 그때그때 다름"],
   "en_choices": ["Morning", "Afternoon", "Evening or night", "It varies across the day"]},
  {"id": "self_flex", "page": "self", "type": "scale10", "required": true,
   "ko": "어떤 일정이 나에게 맞나요?", "en": "What kind of schedule suits you?",
   "ko_low": "정해진 시간에 일하기", "ko_high": "내가 시간을 정하기",
   "en_low": "Fixed, set hours", "en_high": "Choosing my own hours"},
  {"id": "self_people", "page": "self", "type": "scale10", "required": true,
   "ko": "다른 사람과 얼마나 함께 일하는 게 맞나요?", "en": "How much working with others suits you?",
   "ko_low": "주로 혼자", "ko_high": "끊임없는 협업과 회의",
   "en_low": "Mostly alone", "en_high": "Constant collaboration and meetings"},
  {"id": "self_change", "page": "self", "type": "scale10", "required": true,
   "ko": "변화는 어느 정도가 맞나요?", "en": "How much change suits you?",
   "ko_low": "안정적이고 예측 가능한 루틴", "ko_high": "잦은 변화와 돌발 상황",
   "en_low": "A stable, predictable routine", "en_high": "Frequent change and surprises"},
  {"id": "self_pace", "page": "self", "type": "scale10", "required": true,
   "ko": "어떤 속도가 맞나요?", "en": "What pace suits you?",
   "ko_low": "꾸준하고 고른 속도", "ko_high": "강하게 몰아치고 쉬기",
   "en_low": "Steady and even", "en_high": "Intense sprints, then rest"},

  {"id": "a_energy", "page": "job_a", "type": "choice", "required": true,
   "ko": "그 일은 언제 가장 많은 것을 요구했나요?", "en": "When did the work demand the most from you?",
   "ko_choices": ["오전", "오후", "저녁·밤", "하루 전체에 퍼져 있음"],
   "en_choices": ["Morning", "Afternoon", "Evening or night", "Spread across the day"]},
  {"id": "a_flex", "page": "job_a", "type": "scale10", "required": true,
   "ko": "일정은 얼마나 유연했나요?", "en": "How flexible was the schedule?",
   "ko_low": "정해진 시간", "ko_high": "완전히 자유",
   "en_low": "Fixed hours", "en_high": "Fully flexible"},
  {"id": "a_people", "page": "job_a", "type": "scale10", "required": true,
   "ko": "다른 사람과 얼마나 함께 일했나요?", "en": "How much did you work with others?",
   "ko_low": "주로 혼자", "ko_high": "끊임없는 협업과 회의",
   "en_low": "Mostly alone", "en_high": "Constant collaboration and meetings"},
  {"id": "a_change", "page": "job_a", "type": "scale10", "required": true,
   "ko": "일이 얼마나 자주 바뀌었나요?", "en": "How much did things change?",
   "ko_low": "안정적인 루틴", "ko_high": "잦은 변화와 돌발 상황",
   "en_low": "A stable routine", "en_high": "Frequent change and surprises"},
  {"id": "a_pace", "page": "job_a", "type": "scale10", "required": true,
   "ko": "일의 속도는 어땠나요?", "en": "What was the pace?",
   "ko_low": "꾸준하고 고름", "ko_high": "강하게 몰아침",
   "en_low": "Steady and even", "en_high": "Intense sprints"},
  {"id": "a_fit", "page": "job_a", "type": "scale7", "required": true,
   "ko": "전체적으로, 이 일은 내 생활 방식과 얼마나 잘 맞았나요?", "en": "Overall, how well did this job fit the way you live?",
   "ko_low": "전혀 안 맞음", "ko_high": "아주 잘 맞음",
   "en_low": "Not at all", "en_high": "Very well"},
  {"id": "a_adjust", "page": "job_a", "type": "scale10", "required": true,
   "ko": "이 일을 따라가려고 나를 얼마나 맞춰야 했나요?", "en": "How much did you have to adjust yourself to keep up with this job?",
   "ko_low": "전혀", "ko_high": "늘",
   "en_low": "Not at all", "en_high": "Constantly"},
  {"id": "a_check", "page": "job_a", "type": "scale7", "required": true,
   "ko": "꼼꼼히 읽고 계신지 확인하는 문항입니다. 여기서는 4를 골라 주세요.", "en": "To show you're reading carefully, please choose 4 here.",
   "ko_low": "", "ko_high": "", "en_low": "", "en_high": ""},
  {"id": "a_current", "page": "job_a", "type": "choice", "required": true,
   "ko": "지금도 이 일을 하고 있나요?", "en": "Are you still in this job?",
   "ko_choices": ["예", "아니요"], "en_choices": ["Yes", "No"]},
  {"id": "a_duration", "page": "job_a", "type": "choice", "required": true,
   "ko": "이 일을 얼마나 했나요(하고 있나요)?", "en": "How long have you been (or were you) in it?",
   "ko_choices": ["3~6개월", "6~12개월", "1~3년", "3년 이상"],
   "en_choices": ["3–6 months", "6–12 months", "1–3 years", "Over 3 years"]},
  {"id": "a_note", "page": "job_a", "type": "paragraph", "required": false,
   "ko": "(선택) 무엇 때문에 잘 맞았는지, 혹은 안 맞았는지 한두 문장으로 적어 주세요.", "en": "(Optional) In a sentence or two: what made it fit, or not fit?"},
  {"id": "b_opt_in", "page": "job_a", "type": "gate", "required": true,
   "ko": "느낌이 확실히 달랐던 다른 일도 하나 답해 주실 수 있나요? (약 2분)", "en": "Could you also describe one other job that felt clearly different? (about 2 minutes)",
   "ko_choices": ["예", "아니요, 건너뛸게요"], "en_choices": ["Yes", "No, skip this"]},

  {"id": "b_energy", "page": "job_b", "type": "choice", "required": true,
   "ko": "[두 번째 일] 그 일은 언제 가장 많은 것을 요구했나요?", "en": "[Second job] When did the work demand the most from you?",
   "ko_choices": ["오전", "오후", "저녁·밤", "하루 전체에 퍼져 있음"],
   "en_choices": ["Morning", "Afternoon", "Evening or night", "Spread across the day"]},
  {"id": "b_flex", "page": "job_b", "type": "scale10", "required": true,
   "ko": "[두 번째 일] 일정은 얼마나 유연했나요?", "en": "[Second job] How flexible was the schedule?",
   "ko_low": "정해진 시간", "ko_high": "완전히 자유",
   "en_low": "Fixed hours", "en_high": "Fully flexible"},
  {"id": "b_people", "page": "job_b", "type": "scale10", "required": true,
   "ko": "[두 번째 일] 다른 사람과 얼마나 함께 일했나요?", "en": "[Second job] How much did you work with others?",
   "ko_low": "주로 혼자", "ko_high": "끊임없는 협업과 회의",
   "en_low": "Mostly alone", "en_high": "Constant collaboration and meetings"},
  {"id": "b_change", "page": "job_b", "type": "scale10", "required": true,
   "ko": "[두 번째 일] 일이 얼마나 자주 바뀌었나요?", "en": "[Second job] How much did things change?",
   "ko_low": "안정적인 루틴", "ko_high": "잦은 변화와 돌발 상황",
   "en_low": "A stable routine", "en_high": "Frequent change and surprises"},
  {"id": "b_pace", "page": "job_b", "type": "scale10", "required": true,
   "ko": "[두 번째 일] 일의 속도는 어땠나요?", "en": "[Second job] What was the pace?",
   "ko_low": "꾸준하고 고름", "ko_high": "강하게 몰아침",
   "en_low": "Steady and even", "en_high": "Intense sprints"},
  {"id": "b_fit", "page": "job_b", "type": "scale7", "required": true,
   "ko": "[두 번째 일] 전체적으로, 이 일은 내 생활 방식과 얼마나 잘 맞았나요?", "en": "[Second job] Overall, how well did this job fit the way you live?",
   "ko_low": "전혀 안 맞음", "ko_high": "아주 잘 맞음",
   "en_low": "Not at all", "en_high": "Very well"},
  {"id": "b_adjust", "page": "job_b", "type": "scale10", "required": true,
   "ko": "[두 번째 일] 이 일을 따라가려고 나를 얼마나 맞춰야 했나요?", "en": "[Second job] How much did you have to adjust yourself to keep up with this job?",
   "ko_low": "전혀", "ko_high": "늘",
   "en_low": "Not at all", "en_high": "Constantly"},
  {"id": "b_current", "page": "job_b", "type": "choice", "required": true,
   "ko": "[두 번째 일] 지금도 이 일을 하고 있나요?", "en": "[Second job] Are you still in this job?",
   "ko_choices": ["예", "아니요"], "en_choices": ["Yes", "No"]},
  {"id": "b_duration", "page": "job_b", "type": "choice", "required": true,
   "ko": "[두 번째 일] 이 일을 얼마나 했나요(하고 있나요)?", "en": "[Second job] How long have you been (or were you) in it?",
   "ko_choices": ["3~6개월", "6~12개월", "1~3년", "3년 이상"],
   "en_choices": ["3–6 months", "6–12 months", "1–3 years", "Over 3 years"]},
  {"id": "b_note", "page": "job_b", "type": "paragraph", "required": false,
   "ko": "[두 번째 일] (선택) 무엇 때문에 잘 맞았는지, 혹은 안 맞았는지 한두 문장으로 적어 주세요.", "en": "[Second job] (Optional) In a sentence or two: what made it fit, or not fit?"},

  {"id": "work_type", "page": "last", "type": "choice", "required": false,
   "ko": "답한 일과 가장 가까운 것은?", "en": "Which is closest to the work you described?",
   "ko_choices": ["사무·지식 노동", "창작", "현장·서비스", "돌봄·보건·교육", "기타"],
   "en_choices": ["Office or knowledge work", "Creative work", "Hands-on or service work", "Care, health, or education", "Other"]},
  {"id": "region", "page": "last", "type": "choice", "required": false,
   "ko": "주로 어디서 일하나요?", "en": "Where do you mainly work?",
   "ko_choices": ["한국", "한국 밖"], "en_choices": ["Korea", "Outside Korea"]},
  {"id": "source", "page": "last", "type": "choice", "required": false,
   "ko": "이 설문을 어디서 보셨나요?", "en": "Where did you find this survey?",
   "ko_choices": ["지인이 직접 보내줌", "지인이 공유한 글이나 링크", "온라인 커뮤니티", "GitHub", "SurveyCircle", "Reddit", "기타"],
   "en_choices": ["A friend sent it to me", "A post or link someone shared", "An online community", "GitHub", "SurveyCircle", "Reddit", "Other"]},
  {"id": "code_word", "page": "last", "type": "text", "required": false,
   "ko": "(선택) 나중에 응답 삭제를 원할 수도 있다면, 나만 아는 암호 단어를 적어 주세요.", "en": "(Optional) If you might want your answer deleted later, write a code word only you would know."}
];
// END QUESTIONS

const PAGES = {
  "self":  {"ko": ["1부. 나", "아무것도 강요받지 않을 때, 나는 어떻게 일할 때 가장 잘 되는지 떠올려 주세요."],
            "en": ["Part 1. You", "Think about how you work best when nothing forces you otherwise."]},
  "job_a": {"ko": ["2부. 일 하나", "지금 하고 있는 일, 또는 가장 최근에 3개월 이상 했던 일을 떠올려 주세요. 채용 공고에 적힌 모습이 아니라, 실제로 하루하루 어떻게 돌아갔는지를 기준으로 답해 주세요."],
            "en": ["Part 2. A job", "Think of your current job, or the most recent one you did for at least 3 months. Describe how it actually ran day to day, not how it was advertised."]},
  "job_b": {"ko": ["3부. 느낌이 달랐던 다른 일", "첫 번째 일이 잘 안 맞았다면 상대적으로 잘 맞았던 일을, 잘 맞았다면 덜 맞았던 일을 떠올려 주세요. 3개월 이상 했던 일이면 됩니다."],
            "en": ["Part 3. A job that felt different", "If the first job didn't fit you well, think of one that fit better. If it fit well, think of one that fit worse. Any job you did for at least 3 months counts."]},
  "last":  {"ko": ["4부. 마지막 질문 (선택)", ""],
            "en": ["Part 4. Last questions (optional)", ""]}
};

const TEXT = {
  "ko": {
    "title": "지금 하는 일, 내 생활 방식과 잘 맞나요? (약 10분)",
    "intro": "이 설문은 오픈소스 프로젝트 continuum-protocol의 일부입니다. 이 프로젝트는 일이 사람의 능력뿐 아니라 생활의 리듬과도 맞는지를 탐구합니다.\n\n" +
             "- 익명입니다. 이름, 이메일, 회사명, 직함은 묻지 않습니다.\n" +
             "- 약 10분 걸립니다. 언제든 그만둘 수 있고, 제출하기 전에는 아무것도 저장되지 않습니다.\n" +
             "- 요약 결과만 공개합니다. 개별 응답은 공개하지 않습니다.\n" +
             "- 나중에 응답을 지우고 싶을 수도 있다면, 마지막에 나만 아는 암호 단어를 정해 두세요.\n" +
             "- 참여 대상: 만 18세 이상이고, 한 가지 이상의 일(아르바이트·프리랜서 포함)을 3개월 이상 해 본 분.",
    "thanks": "참여해 주셔서 고맙습니다. 요약 결과는 github.com/DevAaronJeong/continuum-protocol 에 올라갑니다. " +
              "응답 삭제를 원하면 이 양식에 암호 단어를 입력해 주세요: "
  },
  "en": {
    "title": "How well does work fit the way you live? (about 10 minutes)",
    "intro": "This survey is part of continuum-protocol, an open-source project that asks whether jobs fit people's rhythms of living, not just their skills.\n\n" +
             "- Anonymous. We don't ask for your name, email, employer, or job title.\n" +
             "- About 10 minutes. You can stop at any point. Nothing is saved until you submit.\n" +
             "- Only summary results are published. Individual answers are never posted.\n" +
             "- If you might want your answer deleted later, choose a code word at the end.\n" +
             "- Who can take part: you're 18 or older and have worked at least one job (part-time and freelance count) for 3 months or more.",
    "thanks": "Thank you for taking part. Summary results will be posted at github.com/DevAaronJeong/continuum-protocol. " +
              "To delete your answer, enter your code word in this form: "
  }
};

function createSurveyForms() {
  const deletion = createDeletionForm_();
  const deletionUrl = deletion.getPublishedUrl();
  const ko = createSurveyForm_("ko", deletionUrl);
  const en = createSurveyForm_("en", deletionUrl);
  Logger.log("Korean survey (share this): " + ko.getPublishedUrl());
  Logger.log("Korean survey (edit):       " + ko.getEditUrl());
  Logger.log("English survey (share this): " + en.getPublishedUrl());
  Logger.log("English survey (edit):       " + en.getEditUrl());
  Logger.log("Deletion form (share this):  " + deletionUrl);
}

function applyPrivacySettings_(form) {
  try { form.setCollectEmail(false); } catch (e) {}
  try { form.setRequireLogin(false); } catch (e) {}
  form.setLimitOneResponsePerUser(false);
  form.setAllowResponseEdits(false);
  form.setPublishingSummary(false);
  form.setShowLinkToRespondAgain(false);
}

function createSurveyForm_(lang, deletionUrl) {
  const t = TEXT[lang];
  const form = FormApp.create(t.title);
  form.setTitle(t.title);
  form.setDescription(t.intro);
  form.setProgressBar(true);
  applyPrivacySettings_(form);
  form.setConfirmationMessage(t.thanks + deletionUrl);

  let currentPage = "intro";
  const pageItems = {};
  let gate = null;
  QUESTIONS.forEach(function (q) {
    if (q.page !== currentPage) {
      const p = PAGES[q.page][lang];
      pageItems[q.page] = form.addPageBreakItem().setTitle(p[0]).setHelpText(p[1]);
      currentPage = q.page;
    }
    const title = q[lang];
    if (q.type === "consent") {
      form.addCheckboxItem().setTitle(title).setChoiceValues(q[lang + "_choices"]).setRequired(true);
    } else if (q.type === "choice") {
      form.addMultipleChoiceItem().setTitle(title).setChoiceValues(q[lang + "_choices"]).setRequired(q.required);
    } else if (q.type === "gate") {
      gate = { item: form.addMultipleChoiceItem().setTitle(title).setRequired(true), choices: q[lang + "_choices"] };
    } else if (q.type === "scale10" || q.type === "scale7") {
      const item = form.addScaleItem().setTitle(title).setRequired(q.required);
      if (q.type === "scale10") { item.setBounds(0, 10); } else { item.setBounds(1, 7); }
      if (q[lang + "_low"] || q[lang + "_high"]) { item.setLabels(q[lang + "_low"], q[lang + "_high"]); }
    } else if (q.type === "paragraph") {
      form.addParagraphTextItem().setTitle(title).setRequired(q.required);
    } else if (q.type === "text") {
      form.addTextItem().setTitle(title).setRequired(q.required);
    }
  });

  // "Yes" goes on to the second job; "No" skips to the last page.
  gate.item.setChoices([
    gate.item.createChoice(gate.choices[0], pageItems["job_b"]),
    gate.item.createChoice(gate.choices[1], pageItems["last"])
  ]);
  return form;
}

function createDeletionForm_() {
  const form = FormApp.create("continuum-protocol 설문 응답 삭제 요청 / Delete my survey answer");
  form.setDescription("설문 마지막에 적은 암호 단어를 입력하면 해당 응답을 삭제합니다.\n" +
                      "Enter the code word you wrote at the end of the survey, and that answer will be deleted.");
  applyPrivacySettings_(form);
  form.addTextItem().setTitle("암호 단어 / Code word").setRequired(true);
  form.setConfirmationMessage("요청을 받았습니다. / Request received.");
  return form;
}
