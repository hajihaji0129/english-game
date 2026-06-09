from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

# =========================
# 초급 50개
# =========================
easy = [
    ("apple", "사과"), ("banana", "바나나"), ("water", "물"), ("book", "책"),
    ("school", "학교"), ("friend", "친구"), ("dog", "개"), ("cat", "고양이"),
    ("house", "집"), ("car", "자동차"), ("sun", "태양"), ("moon", "달"),
    ("star", "별"), ("food", "음식"), ("rice", "밥"), ("milk", "우유"),
    ("hand", "손"), ("head", "머리"), ("eye", "눈"), ("nose", "코"),
    ("mouth", "입"), ("family", "가족"), ("love", "사랑"), ("happy", "행복"),
    ("sad", "슬픈"), ("big", "큰"), ("small", "작은"), ("hot", "더운"),
    ("cold", "추운"), ("good", "좋은"), ("bad", "나쁜"), ("day", "하루"),
    ("night", "밤"), ("morning", "아침"), ("schoolbag", "가방"), ("pen", "펜"),
    ("pencil", "연필"), ("eraser", "지우개"), ("chair", "의자"), ("table", "책상"),
    ("door", "문"), ("window", "창문"), ("tree", "나무"), ("flower", "꽃"),
    ("road", "길"), ("rain", "비"), ("snow", "눈"), ("wind", "바람"),
    ("watermelon", "수박"), ("orange", "오렌지")
]

# =========================
# 중급 50개
# =========================
medium = [
    ("culture", "문화"), ("science", "과학"), ("history", "역사"), ("education", "교육"),
    ("technology", "기술"), ("society", "사회"), ("environment", "환경"), ("information", "정보"),
    ("knowledge", "지식"), ("experiment", "실험"), ("government", "정부"), ("language", "언어"),
    ("computer", "컴퓨터"), ("internet", "인터넷"), ("network", "네트워크"), ("energy", "에너지"),
    ("population", "인구"), ("development", "발전"), ("economy", "경제"), ("industry", "산업"),
    ("research", "연구"), ("question", "질문"), ("answer", "답변"), ("problem", "문제"),
    ("solution", "해결"), ("reason", "이유"), ("result", "결과"), ("process", "과정"),
    ("system", "체계"), ("method", "방법"), ("data", "데이터"), ("service", "서비스"),
    ("product", "제품"), ("company", "회사"), ("market", "시장"), ("business", "사업"),
    ("student", "학생"), ("teacher", "선생님"), ("classroom", "교실"), ("subject", "과목"),
    ("exam", "시험"), ("score", "점수"), ("ability", "능력"), ("skill", "기술"),
    ("experience", "경험"), ("future", "미래"), ("past", "과거"), ("present", "현재"),
    ("change", "변화"), ("growth", "성장")
]

# =========================
# 고급 50개
# =========================
hard = [
    ("philosophy", "철학"), ("psychology", "심리학"), ("economy", "경제"), ("democracy", "민주주의"),
    ("globalization", "세계화"), ("innovation", "혁신"), ("hypothesis", "가설"), ("phenomenon", "현상"),
    ("analysis", "분석"), ("evaluation", "평가"), ("perspective", "관점"), ("interpretation", "해석"),
    ("interaction", "상호작용"), ("communication", "의사소통"), ("civilization", "문명"),
    ("responsibility", "책임"), ("independence", "독립"), ("consciousness", "의식"),
    ("subconscious", "잠재의식"), ("implementation", "실행"), ("representation", "표현"),
    ("transformation", "변형"), ("coordination", "조정"), ("administration", "관리"),
    ("jurisdiction", "관할권"), ("legislation", "법률 제정"), ("constitution", "헌법"),
    ("infrastructure", "기반시설"), ("revolution", "혁명"), ("evolution", "진화"),
    ("motivation", "동기"), ("regulation", "규제"), ("optimization", "최적화"),
    ("standardization", "표준화"), ("mechanism", "메커니즘"), ("phenomenal", "현상적인"),
    ("theoretical", "이론적인"), ("empirical", "경험적인"), ("abstract", "추상적인"),
    ("complexity", "복잡성"), ("variability", "변동성"), ("stability", "안정성"),
    ("adaptation", "적응"), ("resilience", "회복력"), ("sustainability", "지속가능성"),
    ("productivity", "생산성"), ("efficiency", "효율성"), ("compatibility", "호환성"),
    ("validity", "타당성"), ("reliability", "신뢰성"), ("significance", "중요성")
]

# =========================
# 합치기 (150개)
# =========================
words = easy + medium + hard
random.shuffle(words)

# =========================
# 게임 상태
# =========================
game = {
    "score": 0,
    "index": 0,
    "wrong": 0,
    "wrong_list": [],
    "pool": words
}

TOTAL = len(words)

# =========================
# 등급
# =========================
def grade(acc):
    if acc >= 96: return "1등급"
    if acc >= 89: return "2등급"
    if acc >= 77: return "3등급"
    if acc >= 60: return "4등급"
    if acc >= 40: return "5등급"
    if acc >= 23: return "6등급"
    if acc >= 11: return "7등급"
    if acc >= 4: return "8등급"
    return "9등급"

# =========================
# 화면
# =========================
HTML = """
<h2>영어 단어 게임</h2>

<p>점수: {{score}} / 100</p>
<p>진행: {{index}} / {{total}}</p>
<p>틀림: {{wrong}} / 3</p>

{% if not end %}
<h3>뜻: {{word}}</h3>

<form method="POST">
<input name="answer">
<button>제출</button>
</form>

<p>{{result}}</p>

{% else %}
<h2>게임 종료</h2>
<p>점수: {{score}} / 100</p>
<p>정답률: {{acc}}%</p>
<p>등급: {{g}}</p>

<h3>오답노트</h3>
{% for w in wrongs %}
<p>{{w[0]}} - {{w[1]}}</p>
{% endfor %}
{% endif %}
"""

@app.route("/", methods=["GET","POST"])
def home():
    global game

    if game["index"] >= TOTAL or game["wrong"] >= 3:
        acc = round((game["score"]/100)*100,2)
        return render_template_string(HTML,
            score=game["score"],
            index=game["index"],
            total=TOTAL,
            wrong=game["wrong"],
            end=True,
            acc=acc,
            g=grade(acc),
            wrongs=game["wrong_list"]
        )

    word = game["pool"][game["index"]]
    result = ""

    if request.method == "POST":
        ans = request.form.get("answer","").strip().lower()

        if ans == word[0]:
            game["score"] += 2
            result = "정답!"
        else:
            game["wrong"] += 1
            game["wrong_list"].append(word)
            result = f"오답! 정답: {word[0]}"

        game["index"] += 1

    return render_template_string(HTML,
        score=game["score"],
        index=game["index"],
        total=TOTAL,
        wrong=game["wrong"],
        word=word[1],
        result=result,
        end=False
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
