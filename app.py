from flask import Flask, request, render_template_string, session
import random

app = Flask(__name__)
app.secret_key = "english_game_secret"

# =========================
# 단어 (그대로 유지)
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

medium = [
    ("culture", "문화"), ("science", "과학"), ("history", "역사"), ("education", "교육"),
    ("technology", "기술"), ("society", "사회"), ("environment", "환경"), ("information", "정보"),
    ("knowledge", "지식"), ("experiment", "실험"), ("government", "정부"), ("language", "언어"),
    ("computer", "컴퓨터"), ("internet", "인터넷"), ("energy", "에너지"),
    ("population", "인구"), ("economy", "경제"), ("industry", "산업"),
    ("research", "연구"), ("problem", "문제"), ("solution", "해결"),
    ("system", "체계"), ("method", "방법"), ("data", "데이터"),
    ("company", "회사"), ("market", "시장"), ("business", "사업"),
    ("teacher", "선생님"), ("student", "학생"), ("exam", "시험"),
    ("future", "미래"), ("present", "현재"), ("past", "과거"),
    ("change", "변화"), ("growth", "성장")
]

hard = [
    ("philosophy", "철학"), ("psychology", "심리학"), ("economy", "경제"), ("democracy", "민주주의"),
    ("globalization", "세계화"), ("innovation", "혁신"), ("hypothesis", "가설"),
    ("phenomenon", "현상"), ("analysis", "분석"), ("evaluation", "평가"),
    ("perspective", "관점"), ("interpretation", "해석"),
    ("civilization", "문명"), ("responsibility", "책임"),
    ("independence", "독립"), ("consciousness", "의식"),
    ("transformation", "변형"), ("coordination", "조정"),
    ("revolution", "혁명"), ("evolution", "진화"),
    ("optimization", "최적화"), ("mechanism", "메커니즘"),
    ("complexity", "복잡성"), ("adaptation", "적응"),
    ("resilience", "회복력"), ("sustainability", "지속가능성"),
    ("efficiency", "효율성"), ("reliability", "신뢰성")
]

words = easy + medium + hard


# =========================
# UI
# =========================
HTML = """
<style>
body {
    font-family: Arial;
    background: #f4f6f9;
    text-align: center;
}

.card {
    background: white;
    width: 360px;
    margin: 50px auto;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

input {
    padding: 10px;
    width: 80%;
    margin-top: 10px;
}

button {
    padding: 10px 15px;
    margin-top: 10px;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 8px;
}

button:hover {
    background: #45a049;
}
</style>

<div class="card">

<h2>영어 단어 게임</h2>

<p>점수: {{score}} / 100</p>
<p>진행: {{index}} / {{total}}</p>

{% if not end %}
<h3>{{word}}</h3>

<form method="POST">
<input name="answer" autocomplete="off">
<br>
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

<a href="/">다시 시작</a>
{% endif %}

</div>
"""


# =========================
# 게임
# =========================
@app.route("/", methods=["GET", "POST"])
def home():

    if "pool" not in session:
        session["pool"] = random.sample(words, len(words))
        session["index"] = 0
        session["score"] = 0
        session["wrong_list"] = []

    pool = session["pool"]
    index = session["index"]

    # ✔ 종료 조건: 끝까지 도달만
    if index >= len(pool):
        acc = round((session["score"] / 100) * 100, 2)

        return render_template_string(HTML,
            score=session["score"],
            index=index,
            total=len(pool),
            end=True,
            acc=acc,
            g=grade(acc),
            wrongs=session["wrong_list"]
        )

    word = pool[index]
    result = ""

    if request.method == "POST":
        ans = request.form.get("answer", "").strip().lower()

        if ans == word[0]:
            session["score"] += 2
            result = "정답!"
        else:
            session["wrong_list"].append(word)
            result = f"오답! 정답: {word[0]}"

        session["index"] += 1

    return render_template_string(HTML,
        score=session["score"],
        index=session["index"],
        total=len(pool),
        word=word[1],
        result=result,
        end=False
    )


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
