# Continuum Protocol (한국어)

**이력서가 아닌, '삶의 리듬'으로 일과 사람을 연결합니다.**

[![English](https://img.shields.io/badge/Language-English-blue.svg)](README.md)
[![Status](https://img.shields.io/badge/Status-Experimental-orange.svg)]()
[![License](https://img.shields.io/badge/License-Discussing-red.svg)](https://github.com/DevAaronJeong/continuum-protocol/issues)

`continuum-protocol`은 사람과 일이 서로를 소모시키지 않고, 각자의 생활양식(Lifestyle)과 리듬에 맞춰 자연스럽게 정렬(Align)되는 방법을 탐구하는 오픈소스 실험입니다.

우리는 일을 고정된 정체성이 아니라, 삶의 긴 흐름 속에서 잠시 머무는 '**상태(State)**'로 정의합니다.

---

## 🌊 프로젝트의 핵심 철학

### 1. 일에는 절대적인 우열이 없습니다.
대기업, 스타트업, 프리랜서... 어떤 형태가 더 우월한지 따지지 않습니다. 오직 "**지금 내 삶의 리듬과 이 일이 맞는가?**" 만을 봅니다.

### 2. '성실함'의 정의를 바꿉니다.
야근을 많이 하는 것이 성실함이 아닙니다. 자신의 생활 리듬을 건강하게 유지하며 꾸준히 지속하는 **Consistency**이 진짜 역량입니다.

### 3. 떠나는 것은 실패가 아닙니다.
삶의 리듬이 바뀌면, 맞는 일도 바뀝니다. 매칭이 끝나는 것은 실패가 아니라, 서로의 리듬이 달라졌음을 인정하고 자연스럽게 헤어지는 과정입니다.

---

## 📐 개념적 모델 (The Model)

우리는 사람과 직무를 정적인 텍스트가 아닌, **변화하는 Vector**로 바라봅니다.

$$Alignment(t) = f(H_{rhythm}(t), W_{rhythm}(t))$$

여기서 `Rhythm`은 다음 요소들을 포함합니다:
* **에너지 주기:** 아침형 vs 저녁형
* **몰입의 호흡:** 짧고 빠른 스프린트 vs 긴 호흡의 딥워크
* **사회적 밀도:** 고립된 작업 vs 끊임없는 협업
* **변동성 허용:** 루틴한 안정감 vs 예측 불가능한 카오스

> 💡 **코드 예시:** `src/prototype.py`에서 이 벡터들이 어떻게 계산되는지 파이썬 코드로 확인하실 수 있습니다.

---

## 📂 프로젝트 구조
```
continuum-protocol/
├── README.md                  # 영문 문서
├── README.kr.md              # 한글 문서 (여기)
├── MANIFESTO.md              # 핵심 철학
├── docs/
│   ├── ethics-privacy.md     # 프라이버시 & 윤리 원칙
│   ├── why-not-job-board.md  # 기존 잡보드와의 차이점
│   ├── open-questions.md     # 미해결 질문들 (도와주세요!)
│   └── roadmap.md            # 앞으로의 방향
├── examples/
│   ├── simple_match.py       # 빠른 데모 (먼저 실행해보세요!)
│   └── synthetic_data.py     # 테스트 데이터 생성기
└── src/
    └── prototype.py          # 핵심 매칭 로직
```

---

## 🚀 빠른 시작

### 데모 실행하기
```bash
# 저장소 복제
git clone https://github.com/DevAaronJeong/continuum-protocol.git
cd continuum-protocol

# 간단한 매칭 예제 실행
python examples/simple_match.py

# 합성 데이터 생성
python examples/synthetic_data.py
```

### 문서 읽기

📖 **프로젝트가 처음이신가요?**
1. [MANIFESTO.md](MANIFESTO.md)부터 읽어보세요 - 핵심 철학
2. [docs/why-not-job-board.md](docs/why-not-job-board.md) - 어떻게 다른가
3. [docs/ethics-privacy.md](docs/ethics-privacy.md) - 프라이버시 원칙

🤔 **우려사항이나 질문이 있으신가요?**
- [docs/open-questions.md](docs/open-questions.md) 참고
- `philosophy` 또는 `ethics` 태그로 이슈 열어주세요

🛠️ **기여하고 싶으신가요?**
- [CONTRIBUTING.md](CONTRIBUTING.md) 읽기
- [docs/roadmap.md](docs/roadmap.md) 확인

---

## 🚫 윤리적 원칙 (Ethics First)

**이 시스템이 만약 감시 도구가 된다면, 실패한 것입니다.**

- 데이터는 전적으로 사용자가 소유합니다
- 분석은 가능한 로컬에서 이루어집니다
- 매칭 이유는 항상 설명 가능해야 합니다
- 언제든 옵트아웃 가능해야 합니다

📄 자세한 내용: [docs/ethics-privacy.md](docs/ethics-privacy.md)

---

## 🧪 미해결 질문들

이 프로젝트는 의도적으로 불완전합니다. 우리가 답을 모르는 질문들:

- 생활양식 프로파일링이 감시가 되지 않을 수 있을까?
- "노력"을 시간이 아닌 다른 방식으로 측정할 수 있을까?
- 조직을 공정하게 평가하는 방법은?
- 언제 매칭을 종료해야 할까?

💬 [docs/open-questions.md](docs/open-questions.md)에서 더 많은 질문을 보고, 여러분의 생각을 나눠주세요.

---

## 🤝 참여하기

이 철학에 동의하시나요? 혹은 말이 안 된다고 생각하시나요?  
**어떤 의견이든 환영합니다.**

- 🗣️ [GitHub Discussions](https://github.com/DevAaronJeong/continuum-protocol/discussions)에서 토론
- 🐛 [Issues](https://github.com/DevAaronJeong/continuum-protocol/issues)에 의견 남기기
- 📝 한국어 이슈 환영합니다
- 💻 코드 기여: [CONTRIBUTING.md](CONTRIBUTING.md) 참고

---

## 💬 자주 묻는 질문

**Q: 이게 잡보드인가요?**  
A: 아닙니다. 생활양식 간의 정렬을 모델링하는 프로토콜입니다.

**Q: 프라이버시는 어떻게 보호하나요?**  
A: 분석은 로컬에서, 데이터는 사용자가 소유합니다. [docs/ethics-privacy.md](docs/ethics-privacy.md) 참고.

**Q: 실제로 사용할 수 있나요?**  
A: 아직 실험 단계입니다. 프로덕션 사용은 권장하지 않습니다.

**Q: 어디서 시작해야 하나요?**  
A: [MANIFESTO.md](MANIFESTO.md)를 먼저 읽고, [docs/](docs/) 폴더를 탐색하세요.

**Q: 지금 써볼 수 있나요?**  
A: 네! `python examples/simple_match.py`를 실행해보세요.

---

## 🙏 감사의 말

이 프로젝트는 다음의 토대 위에 서 있습니다:
* **Ambient Intelligence** 연구
* **Human-Computer Interaction** 윤리학
* **안티-허슬(Anti-hustle)** 운동
* 전통적 고용 모델에 의문을 제기하는 모든 분들

---

**이것은 잡보드가 아닙니다.**  
**이것은 전환을 존중하는 시스템입니다.**

---

*최종 업데이트: 2025*