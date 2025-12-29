# Continuum Protocol (한국어)

**이력서가 아닌, '삶의 리듬'으로 일과 사람을 연결합니다.**

[![English](https://img.shields.io/badge/Language-English-blue.svg)](README.md)
[![Status](https://img.shields.io/badge/Status-Experimental-orange.svg)]()
[![License](https://img.shields.io/badge/License-Discussing-red.svg)](https://github.com/DevAaronJeong/continuum-protocol/issues)

`continuum-protocol`은 사람과 일이 서로를 소모시키지 않고, 각자의 생활양식(Lifestyle)과 리듬에 맞춰 자연스럽게 정렬(Align)되는 방법을 탐구하는 오픈소스 실험입니다.

우리는 일을 고정된 정체성이 아니라, 삶의 긴 흐름 속에서 잠시 머무는 '**State**'로 정의합니다.

---

## 🌊 프로젝트의 핵심 철학

### 1. 일에는 절대적인 우열이 없습니다.
대기업, 스타트업, 프리랜서... 어떤 형태가 더 우월한지 따지지 않습니다. 오직 "**지금 내 삶의 리듬과 이 일이 맞는가?**" 만을 봅니다.

### 2. '성실함'의 정의를 바꿉니다.
야근을 많이 하는 것이 성실함이 아닙니다. 자신의 생활 리듬을 건강하게 유지하며 꾸준히 지속하는 **Consistency**이 진짜 역량입니다.

### 3. 떠나는 것은 실패가 아닙니다.
삶의 리듬이 바뀌면, 맞는 일도 바뀝니다. 매칭이 끝나는 것은 실패가 아니라, 서로의 리듬이 달라졌음을 인정하고 자연스럽게 헤어지는 과정입니다.

---

## 📐 수학적 모델 (개념적)

**중요:** 이 시스템은 코사인 유사도가 아닌, 가중치 기반 거리 측정을 사용합니다.

사람($H$)과 일($W$)을 여러 차원을 가진 벡터로 모델링합니다:

$$H = (h_1, h_2, h_3, ..., h_n)$$
$$W = (w_1, w_2, w_3, ..., w_n)$$

각 차원은 생활양식 속성(에너지 리듬, 유연성 등)을 나타냅니다.

**Alignment Score**는 다음과 같이 계산됩니다:

$$Alignment = 1 - \sum_{i=1}^{n} \alpha_i \cdot |h_i - w_i|$$

여기서:
- $\alpha_i$ = 차원 $i$의 가중치 (모든 가중치의 합은 1)
- $|h_i - w_i|$ = 차원 $i$의 절대 차이

**왜 이 방식인가?**
1. **해석 가능성**: 각 차원이 독립적으로 기여
2. **자연스러운 스케일링**: 자동으로 [0, 1] 범위의 점수 생성
3. **조정 가능성**: 차원별 가중치 조정이 쉬움
4. **설명 가능성**: 어떤 차원이 일치/불일치하는지 정확히 표시

**시간 인식:**

$$Alignment(t) = f(H(t), W(t), Context(t))$$

핵심 통찰: 정렬은 특정 순간 $t$에 계산되며, 사람과 일 모두 시간에 따라 진화함을 인정합니다.

💻 **코드 보기:** 상세한 주석이 포함된 실제 구현은 `src/alignment_engine.py`를 확인하세요.

---

## 🧘 선언문 & 철학

1. **생활양식에는 우열이 없습니다.** (저녁형 인간 $\neq$ 게으름)
2. **일관성이 노력입니다.** (리듬 유지 > 번아웃)
3. **일은 역할이지, 정체성이 아닙니다.** (들어갔다 나오는 것)
4. **떠나는 것은 실패가 아닙니다.** (그저 상태 변화일 뿐)

📖 전체 내용: [MANIFESTO.md](MANIFESTO.md)

---

## 🐍 왜 Python인가?

**이것은 머신러닝 프로젝트가 아닙니다.**

Python을 사용하는 이유:
- **가독성**: 코드는 최적화보다 이해 가능해야 함
- **접근성**: 대부분의 개발자가 읽고 비판할 수 있음
- **프로토타이핑**: 개념적 아이디어의 빠른 반복

이 실험들은 **성능보다 명확성**을 우선합니다. 만약 프로덕션 코드였다면 언어 선택이 중요했겠지만, 탐색적 연구이므로 Python의 표현력이 속도보다 가치 있습니다.

---

## 🧪 코드 실험

이 저장소는 작고 독립적인 Python 실험들을 포함합니다.  
**이것들은 제품 구현이 아니라**, 정렬이 코드로 어떻게 표현될 수 있는지에 대한 탐구입니다.

### 사용 가능한 실험들

**`src/alignment_engine.py`**  
사람과 일을 생활양식 벡터로 모델링하고, 그들의 정렬을 비교하는 최소 모델
- 실행: `python src/alignment_engine.py`
- 목적: 실행 가능한 형태로 핵심 개념 시연
- 상태: 개념적 프로토타입 (프로덕션 준비 안됨)

**`examples/simple_match.py`**  
좋은 정렬 vs 나쁜 정렬 두 시나리오를 보여주는 기본 예제
- 실행: `python examples/simple_match.py`
- 목적: 리듬 호환성에 따라 같은 로직이 다른 결과를 만드는 것 표시

**`examples/batch_alignment_demo.py`**  
한 사람의 프로필을 여러 일 기회와 매칭하는 예제
- 실행: `python examples/batch_alignment_demo.py`
- 목적: 순위가 절대적이 아닌 맥락적임을 설명

**`examples/synthetic_data.py`**  
테스트용 가짜 생활양식 프로필 생성
- 실행: `python examples/synthetic_data.py`
- 목적: 실제 사용자 정보 없이 테스트 데이터 생성

### 이 실험들이 아닌 것

❌ 프로덕션 준비 코드  
❌ AI/ML 구현  
❌ 채용 도구  
❌ 완전한 솔루션  

### 이 실험들인 것

✅ 코드로 표현된 사고 실험  
✅ 비판과 개선을 위한 초대  
✅ "일을 상태로" 탐구하기 위한 시작점  
✅ 설명 가능성 시연 (항상 "왜"를 보여줌)  

### 피드백 환영

이 실험들은 의도적으로 불완전합니다. 다음을 발견하시면:
- 잘못된 가정
- 누락된 차원
- 더 나은 접근법
- 윤리적 우려

이슈를 열어주세요. 비판이 칭찬보다 가치 있습니다.

---

## 📂 프로젝트 구조

```
continuum-protocol/
├── README.md                       # 영문 문서
├── README.kr.md                   # 한글 문서 (여기)
├── MANIFESTO.md                   # 핵심 철학
├── docs/
│   ├── ethics-privacy.md          # 프라이버시 & 윤리 원칙
│   ├── why-not-job-board.md       # 기존 잡보드와의 차이점
│   ├── open-questions.md          # 미해결 질문들 (도와주세요!)
│   └── roadmap.md                 # 앞으로의 방향
├── src/
│   └── alignment_engine.py        # 핵심 정렬 로직 (개념적)
├── examples/
│   ├── simple_match.py            # 기본 정렬 데모
│   ├── batch_alignment_demo.py    # 다중 옵션 매칭
│   └── synthetic_data.py          # 테스트 데이터 생성기
├── .github/
│   └── ISSUE_TEMPLATE/            # 이슈 템플릿
└── requirements.txt               # 의존성 (현재 없음)
```

---

## 🚀 빠른 시작

### 데모 실행하기

```bash
# 저장소 복제
git clone https://github.com/DevAaronJeong/continuum-protocol.git
cd continuum-protocol

# 메인 정렬 데모 실행
python src/alignment_engine.py

# 배치 매칭 시도
python examples/batch_alignment_demo.py

# 합성 테스트 데이터 생성
python examples/synthetic_data.py
```

### 문서 읽기

📖 **프로젝트가 처음이신가요?**
1. [MANIFESTO.md](MANIFESTO.md)부터 시작 - 핵심 철학
2. [docs/why-not-job-board.md](docs/why-not-job-board.md) 읽기 - 어떻게 다른가
3. [docs/ethics-privacy.md](docs/ethics-privacy.md) 확인 - 프라이버시 원칙

🤔 **우려사항이나 질문이 있으신가요?**
- [docs/open-questions.md](docs/open-questions.md) 참고
- `philosophy` 또는 `ethics` 태그로 이슈 열기

🛠️ **기여하고 싶으신가요?**
- [CONTRIBUTING.md](CONTRIBUTING.md) 읽기
- [docs/roadmap.md](docs/roadmap.md) 확인

---

## 🚫 윤리 우선 (Ethics First)

**이 시스템이 만약 감시 도구가 된다면, 실패한 것입니다.**

- 데이터는 전적으로 사용자가 소유합니다
- 분석은 가능한 로컬에서 이루어집니다
- 매칭 이유는 항상 설명 가능해야 합니다
- 언제든 옵트아웃 가능해야 합니다

📄 자세한 내용: [docs/ethics-privacy.md](docs/ethics-privacy.md)

---

## 🔮 미래 실험 (미해결 질문)

이것들은 의도적으로 정의되지 않았습니다. 우리는 아직 답을 모릅니다.

### 잠재적 탐구 영역

**시간적 정렬**
- 시간에 따라 정렬이 어떻게 변하는가?
- 시스템은 언제 재평가를 제안해야 하는가?
- 정렬 drift를 예측할 수 있는가?

**종료 조건**
- 어떤 신호가 정렬이 악화되고 있음을 나타내는가?
- "일시적 어려움"과 "근본적 불일치"를 어떻게 구분하는가?
- 언제 이탈을 제안해야 하는가?

**비수치적 표현**
- 리듬을 정량화 없이 포착할 수 있는가?
- 우리가 놓치고 있는 생활양식 차원이 있는가?
- 문화적 또는 맥락적 요인을 어떻게 모델링하는가?

**조직 프로파일링**
- 회사의 실제 리듬을 어떻게 측정하는가 (주장된 문화가 아닌)?
- 팀 역학을 윤리적으로 벡터화할 수 있는가?
- 시스템 조작을 무엇이 방지하는가?

**프라이버시 보존 매칭**
- 연합 학습 접근법?
- 정렬 점수의 차등 프라이버시?
- 사용자 제어 프로파일링 세분성?

---

**이것들은 로드맵 항목이 아닙니다.** 미해결 연구 질문입니다.

아이디어, 비판, 또는 이 중 하나를 탐구하고 싶다면 이슈나 토론을 열어주세요.

---

## 🤔 자주 묻는 질문

**Q: 이게 잡보드인가요?**  
A: 아닙니다. 생활양식 간의 정렬을 모델링하는 프로토콜입니다.

**Q: 코드를 사용할 수 있나요?**  
A: 네, 하지만 개념적 프로토타입입니다. 상당한 개발 없이 프로덕션에 사용하지 마세요.

**Q: 왜 코드가 이렇게 단순한가요?**  
A: 의도적입니다. 이것은 탐색적이지, 최적화된 것이 아닙니다. 복잡성은 핵심 아이디어를 가릴 것입니다.

**Q: 뭐가 빠져있나요?**  
A: 거의 모든 것. 프라이버시 구현, 실제 데이터 수집, 검증, 확장성, UI 등. [docs/open-questions.md](docs/open-questions.md) 참고.

**Q: 어디서 시작해야 하나요?**  
A: [MANIFESTO.md](MANIFESTO.md)를 먼저 읽고, `python src/alignment_engine.py`를 실행하세요.

**Q: 왜 Python이고 [다른 언어]가 아닌가요?**  
A: 성능보다 가독성. 이것은 연구이지 프로덕션이 아닙니다. 위의 [왜 Python인가?](#-왜-python인가) 섹션 참고.

---

## 💬 커뮤니티

* **토론:** [GitHub Discussions](https://github.com/DevAaronJeong/continuum-protocol/discussions)
* **철학 질문:** `philosophy` 태그 사용
* **기술 질문:** `technical` 태그 사용
* **한국어 이슈 환영합니다**

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
