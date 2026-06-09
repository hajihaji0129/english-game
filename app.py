from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

# =========================
# 단어 150개 (초/중/고)
# =========================
words = [
    {"english": "apple", "korean": "사과"},
    {"english": "banana", "korean": "바나나"},
    {"english": "water", "korean": "물"},
    {"english": "school", "korean": "학교"},
    {"english": "friend", "korean": "친구"},
    {"english": "dog", "korean": "개"},
    {"english": "cat", "korean": "고양이"},
    {"english": "book", "korean": "책"},
    {"english": "car", "korean": "자동차"},
    {"english": "house", "korean": "집"},

    {"english": "culture", "korean": "문화"},
    {"english": "science", "korean": "과학"},
    {"english": "history", "korean": "역사"},
    {"english": "technology", "korean": "기술"},
    {"english": "education", "korean": "교육"},
    {"english": "society", "korean": "사회"},
    {"english": "environment", "korean": "환경"},
    {"english": "knowledge", "korean": "지식"},
    {"english": "experiment", "korean": "실험"},
    {"english": "information", "korean": "정보"},

    {"english": "hypothesis", "korean": "가설"},
    {"english": "phenomenon", "korean": "현상"},
    {"english": "philosophy", "korean": "철학"},
    {"english": "psychology", "korean": "심리학"},
    {"english": "economy", "korean": "경제"},
    {"english": "democracy", "korean": "민주주의"},
    {"english": "globalization", "korean": "세계화"},
    {"english": "innovation", "korean": "혁신"},
    {"english": "analysis", "korean": "분석"},
    {"english": "evaluation", "korean": "평가"},
]

# =========================
# 게임 상태
# =========================
game = {
    "score": 0,
    "index": 0,
    "wrong": 0,
    "wrong_list": [],
    "pool": random.sample(words, len(words))
}

TOTAL = len(words)

# =========================
# HTML
# =========================
HTML = """
<h2>영어 단어 게임</h2>

<p>점수: {{score}} / 100</p>
<p>진행: {{index}} / {{total}}</p>
<p>틀림: {{wrong}} / 3</p>

{% if not game_over %}
    <h3>뜻: {{word}}</h3>

    <form method="POST">
        <input name="answer" autocomplete="off">
        <button type="submit">제출</button>
    </form>

    <p>{{result}}</p>

{% else %}
    <h2>게임 종료</h2>
    <p>최종 점수: {{score}} / 100</p>
    <p>정답률: {{accuracy}}%</p>
    <p>등급: {{grade}}</p>

    <h3>오답노트</h3>
    {% for w in wrong_list %}
        <p>{{w.english}} - {{w.korean}}</p>
    {% endfor %}
{% endif %}
"""

# =========================
# 등급 함수
# =========================
def get_grade(acc):
    if acc >= 96:
        return "1등급"
    elif acc >= 89:
        return "2등급"
    elif acc >= 77:
        return "3등급"
    elif acc >= 60:
        return "4등급"
    elif acc >= 40:
        return "5등급"
    elif acc >= 23:
        return "6등급"
    elif acc >= 11:
        return "7등급"
    elif acc >= 4:
        return "8등급"
    else:
        return "9등급"

# =========================
# 메인
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    global game

    if game["index"] >= TOTAL or game["wrong"] >= 3:
        accuracy = round((game["score"] / 100) * 100, 2)
        grade = get_grade(accuracy)

        return render_template_string(
            HTML,
            score=game["score"],
            wrong=game["wrong"],
            index=game["index"],
            total=TOTAL,
            game_over=True,
            accuracy=accuracy,
            grade=grade,
            wrong_list=game["wrong_list"]
        )

    word = game["pool"][game["index"]]
    result = ""

    if request.method == "POST":
        answer = request.form.get("answer", "").strip()

        if answer.lower() == word["english"]:
            game["score"] += 2
            result = "정답!"
        else:
            game["wrong"] += 1
            game["wrong_list"].append(word)
            result = f"오답! 정답: {word['english']}"

        game["index"] += 1

    return render_template_string(
        HTML,
        score=game["score"],
        wrong=game["wrong"],
        index=game["index"],
        total=TOTAL,
        word=word["korean"],
        result=result,
        game_over=False
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
