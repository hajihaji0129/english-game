from flask import Flask, request, render_template_string, redirect
import random
import time

app = Flask(__name__)

# =========================
# 초급 50개
# =========================
easy = [
    ("apple","사과"),("banana","바나나"),("water","물"),("milk","우유"),("bread","빵"),
    ("school","학교"),("teacher","선생님"),("student","학생"),("book","책"),("pencil","연필"),
    ("eraser","지우개"),("desk","책상"),("chair","의자"),("friend","친구"),("family","가족"),
    ("mother","어머니"),("father","아버지"),("dog","개"),("cat","고양이"),("bird","새"),
    ("fish","물고기"),("house","집"),("room","방"),("door","문"),("window","창문"),
    ("car","자동차"),("bus","버스"),("train","기차"),("road","길"),("tree","나무"),
    ("flower","꽃"),("sun","태양"),("moon","달"),("star","별"),("rain","비"),
    ("snow","눈"),("big","큰"),("small","작은"),("good","좋은"),("bad","나쁜"),
    ("happy","행복한"),("sad","슬픈"),("hot","뜨거운"),("cold","차가운"),("red","빨간"),
    ("blue","파란"),("green","초록"),("run","달리다"),("walk","걷다"),("food","음식")
]

# =========================
# 중급 50개
# =========================
medium = [
    ("culture","문화"),("society","사회"),("history","역사"),("future","미래"),("environment","환경"),
    ("technology","기술"),("knowledge","지식"),("education","교육"),("science","과학"),("experiment","실험"),
    ("information","정보"),("communication","의사소통"),("decision","결정"),("problem","문제"),("solution","해결책"),
    ("success","성공"),("failure","실패"),("journey","여행"),("adventure","모험"),("energy","에너지"),
    ("nature","자연"),("health","건강"),("exercise","운동"),("danger","위험"),("safety","안전"),
    ("respect","존중"),("honest","정직한"),("create","창조하다"),("develop","발전시키다"),("discover","발견하다"),
    ("protect","보호하다"),("achieve","성취하다"),("improve","향상시키다"),("participate","참여하다"),("maintain","유지하다"),
    ("compare","비교하다"),("analyze","분석하다"),("explain","설명하다"),("describe","묘사하다"),("suggest","제안하다"),
    ("prefer","선호하다"),("increase","증가하다"),("decrease","감소하다"),("prepare","준비하다"),("imagine","상상하다"),
    ("realize","깨닫다"),("support","지원하다"),("method","방법"),("process","과정"),("system","체계")
]

# =========================
# 고급 50개
# =========================
hard = [
    ("hypothesis","가설"),("phenomenon","현상"),("philosophy","철학"),("psychology","심리학"),("sociology","사회학"),
    ("democracy","민주주의"),("economy","경제"),("globalization","세계화"),("innovation","혁신"),("civilization","문명"),
    ("perspective","관점"),("analysis","분석"),("interpretation","해석"),("evaluation","평가"),("consequence","결과"),
    ("circumstance","상황"),("significant","중요한"),("essential","필수적인"),("complex","복잡한"),("efficient","효율적인"),
    ("accurate","정확한"),("controversy","논란"),("legislation","법률"),("infrastructure","기반시설"),("mechanism","메커니즘"),
    ("paradigm","패러다임"),("ethical","윤리적인"),("cognitive","인지의"),("regulate","규제하다"),("emphasize","강조하다"),
    ("demonstrate","입증하다"),("investigate","조사하다"),("establish","확립하다"),("generate","생성하다"),("contribute","기여하다"),
    ("sustain","유지하다"),("framework","틀"),("dimension","차원"),("variable","변수"),("algorithm","알고리즘"),
    ("optimization","최적화"),("transformation","변형"),("implementation","실행"),("representation","표현"),("coordination","조정"),
    ("administration","관리"),("revolution","혁명"),("evolution","진화"),("resilience","회복력"),("productivity","생산성")
]

words = easy + medium + hard  # 👉 정확히 150개
random.shuffle(words)

# =========================
# 게임 상태
# =========================
game = {
    "started": False,
    "words": [],
    "index": 0,
    "score": 0,
    "wrong": 0,
    "wrong_list": [],
    "mode": "1",
    "current_answer": "",
    "start_time": 0,
    "total_time": 0,
    "questions": 0
}

MAX_WRONG = 3

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
# UI
# =========================
HTML = """
<h2>영어 단어 게임</h2>

{% if not game.started %}
<form method="POST" action="/start">

<h3>난이도</h3>
<select name="level">
<option value="전체">전체</option>
<option value="초급">초급</option>
<option value="중급">중급</option>
<option value="고급">고급</option>
</select>

<h3>모드</h3>
<select name="mode">
<option value="1">뜻 → 영어</option>
<option value="2">영어 → 뜻</option>
</select>

<button>시작</button>
</form>

{% else %}

<p>점수: {{game.score}} / 100</p>
<p>틀림: {{game.wrong}} / 3</p>
<p>진행: {{game.index}} / {{total}}</p>

<h3>{{question}}</h3>
<p>글자 수: {{length}}</p>

<form method="POST" action="/answer">
<input name="answer" autocomplete="off">
<button>제출</button>
</form>

{% endif %}

{% if end %}
<h2>게임 종료</h2>
<p>점수: {{game.score}} / 100</p>
<p>정답률: {{acc}}%</p>
<p>평균 시간: {{avg}}초</p>
<p>등급: {{grade}}</p>

<h3>오답노트</h3>
{% for w in game.wrong_list %}
<p>{{w[0]}} - {{w[1]}}</p>
{% endfor %}

<a href="/restart"><button>다시 시작</button></a>
{% endif %}
"""

# =========================
# 시작
# =========================
@app.route("/")
def index():
    if not game["started"]:
        return render_template_string(HTML, game=game)

    if game["wrong"] >= MAX_WRONG or game["index"] >= len(game["words"]):
        acc = round((game["score"]/100)*100,2)
        avg = game["total_time"]/game["questions"] if game["questions"] else 0

        return render_template_string(HTML,
            game=game,
            end=True,
            acc=acc,
            avg=round(avg,2),
            grade=grade(acc)
        )

    w = game["words"][game["index"]]

    if game["mode"] == "1":
        question = w[1]
        answer = w[0]
    else:
        question = w[0]
        answer = w[1]

    game["current_answer"] = answer
    game["start_time"] = time.time()

    return render_template_string(
        HTML,
        game=game,
        question=question,
        length=len(w[0]),
        total=len(game["words"]),
        end=False
    )

# =========================
# 시작 세팅
# =========================
@app.route("/start", methods=["POST"])
def start():
    level = request.form["level"]
    mode = request.form["mode"]

    filtered = [w for w in words if level == "전체" or
                (level == "초급" and w in easy) or
                (level == "중급" and w in medium) or
                (level == "고급" and w in hard)]

    random.shuffle(filtered)

    game["started"] = True
    game["words"] = filtered
    game["index"] = 0
    game["score"] = 0
    game["wrong"] = 0
    game["wrong_list"] = []
    game["mode"] = mode
    game["total_time"] = 0
    game["questions"] = 0

    return redirect("/")

# =========================
# 답
# =========================
@app.route("/answer", methods=["POST"])
def answer():
    ans = request.form["answer"].strip().lower()

    t = time.time() - game["start_time"]
    game["total_time"] += t
    game["questions"] += 1

    if ans == game["current_answer"].lower():
        game["score"] += 2
    else:
        game["wrong"] += 1
        game["wrong_list"].append(game["words"][game["index"]])

    game["index"] += 1

    return redirect("/")

# =========================
# 리셋
# =========================
@app.route("/restart")
def restart():
    game["started"] = False
    return redirect("/")

# =========================
# 실행
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
