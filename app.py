from flask import Flask, request, render_template_string, session, redirect, url_for
import random
import time

app = Flask(__name__)
# Render 배포 환경에서는 보안을 위해 secret_key가 필수적이며, 세션 암호화에 사용됩니다.
app.secret_key = "english_game_final_key_v2"

# =========================
# 단어 데이터 (코드 가독성을 위해 상위 일부만 표기, 기존 150개 데이터 그대로 유지하시면 됩니다)
# =========================
easy = [
("apple","사과"),("banana","바나나"),("water","물"),("book","책"),("school","학교"),
("friend","친구"),("dog","개"),("cat","고양이"),("house","집"),("car","자동차"),
("sun","태양"),("moon","달"),("star","별"),("food","음식"),("rice","밥"),
("milk","우유"),("hand","손"),("head","머리"),("eye","눈"),("nose","코"),
("mouth","입"),("family","가족"),("love","사랑"),("happy","행복"),("sad","슬픈"),
("big","큰"),("small","작은"),("hot","더운"),("cold","추운"),("good","좋은"),
("bad","나쁜"),("day","하루"),("night","밤"),("morning","아침"),("pen","펜"),
("pencil","연필"),("chair","의자"),("table","책상"),("door","문"),("window","창문"),
("tree","나무"),("flower","꽃"),("rain","비"),("snow","눈"),("wind","바람"),
("road","길"),("train","기차"),("bus","버스"),("watermelon","수박"),("orange","오렌지")
]

medium = [
("culture","문화"),("science","과학"),("history","역사"),("education","교육"),("technology","기술"),
("society","사회"),("environment","환경"),("information","정보"),("knowledge","지식"),("experiment","실험"),
("government","정부"),("language","언어"),("computer","컴퓨터"),("internet","인터넷"),("energy","에너지"),
("population","인구"),("economy","경제"),("industry","산업"),("research","연구"),("problem","문제"),
("solution","해결"),("system","체계"),("method","방법"),("data","데이터"),("company","회사"),
("market","시장"),("business","사업"),("student","학생"),("teacher","선생님"),("exam","시험"),
("future","미래"),("present","현재"),("past","과거"),("change","변화"),("growth","성장"),
("ability","능력"),("skill","기술"),("experience","경험"),("project","프로젝트"),("community","공동체"),
("transport","교통"),("hospital","병원"),("weather","날씨"),("season","계절"),("communication","소통"),
("opinion","의견"),("decision","결정"),("reason","이유"),("result","결과"),("process","과정")
]

hard = [
("philosophy","철학"),("psychology","심리학"),("economy","경제"),("democracy","민주주의"),("globalization","세계화"),
("innovation","혁신"),("hypothesis","가설"),("phenomenon","현상"),("analysis","분석"),("evaluation","평가"),
("perspective","관점"),("interpretation","해석"),("civilization","문명"),("responsibility","책임"),("independence","독립"),
("consciousness","의식"),("transformation","변형"),("coordination","조정"),("revolution","혁명"),("evolution","진화"),
("optimization","최적화"),("mechanism","메커니즘"),("complexity","복잡성"),("adaptation","적응"),("resilience","회복력"),
("sustainability","지속가능성"),("efficiency","효율성"),("reliability","신뢰성"),("jurisdiction","관할권"),("legislation","법률"),
("infrastructure","기반시설"),("administration","행정"),("constitution","헌법"),("empirical","경험적인"),("theoretical","이론적인"),
("paradigm","패러다임"),("quantitative","정량적인"),("qualitative","정성적인"),("analyze","분석하다"),("implement","실행하다"),
("synthesize","종합하다"),("validate","검증하다"),("framework","틀"),("dimension","차원"),("variable","변수"),
("algorithm","알고리즘"),("optimization","최적화"),("structure","구조"),("concept","개념"),("theory","이론")
]

# =========================
# 등급 산출 함수
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
# UI (HTML Template)
# =========================
HTML = """
<style>
body { font-family: Arial; background:#f4f6f9; text-align:center; }
.card { background:white; width:380px; margin:50px auto; padding:25px; border-radius:12px;
box-shadow:0 4px 10px rgba(0,0,0,0.1);}
input, select { padding:10px; width:80%; margin-top:8px; }
button { padding:10px 15px; margin-top:10px; cursor:pointer; }
.result-msg { font-weight: bold; margin-top: 15px; color: #2c3e50; }
</style>

<div class="card">
<h2>영어 단어 게임</h2>

{% if step == "start" %}
    <form method="POST">
    <h3>난이도</h3>
    <select name="level">
    <option value="easy">초급</option>
    <option value="medium">중급</option>
    <option value="hard">고급</option>
    </select>

    <h3>모드</h3>
    <select name="mode">
    <option value="1">뜻 → 영어</option>
    <option value="2">영어 → 뜻</option>
    </select>

    <button name="action" value="start">시작</button>
    </form>

{% elif step == "quiz" %}
    <p>점수: {{score}} / 100</p>
    <p>진행: {{idx}} / 50</p>

    <h3>{{question}}</h3>
    <p style="color:gray;">글자 수 힌트: {{hint}}자</p>

    {% if result %}
        <p class="result-msg">{{result}}</p>
    {% endif %}

    <form method="POST">
    <input name="answer" autocomplete="off" autofocus onkeydown="if(event.key==='Enter'){this.form.submit();}">
    <button>제출</button>
    </form>

    <br>
    <form method="POST">
    <button name="action" value="restart">처음으로</button>
    </form>

{% else %}
    <h2>게임 종료</h2>
    <p>점수: {{score}} / 100</p>
    <p>정답률: {{acc}}%</p>
    <p>등급: {{g}}</p>
    <p>평균 반응 시간: {{avg}}초</p>

    <h3>오답노트</h3>
    {% for w in wrong %}
    <p>{{w[0]}} - {{w[1]}}</p>
    {% endfor %}

    <form method="POST">
    <button name="action" value="restart">처음으로</button>
    </form>
{% endif %}
</div>
"""

# =========================
# 메인 라우터
# =========================
@app.route("/", methods=["GET", "POST"])
def home():
    # 사용자의 현재 세션 상태 확인 (없으면 start로 강제 지정)
    if "step" not in session:
        session["step"] = "start"

    if request.method == "POST":
        action = request.form.get("action")
        
        # 1. 처음으로 (다시 시작) 버튼 클릭 시 세션 초기화
        if action == "restart":
            session.clear()
            return redirect(url_for("home"))

        # 2. 게임 시작 버튼 클릭 시 각 사용자 전용 세션 데이터 생성
        if action == "start" and session["step"] == "start":
            level = request.form.get("level")
            mode = request.form.get("mode")

            if level == "easy":
                pool = easy[:]
            elif level == "medium":
                pool = medium[:]
            else:
                pool = hard[:]

            random.shuffle(pool)
            pool = pool[:50]  # 50개 선택

            # 사용자 세션(사물함)에 게임 정보 독립 저장
            session["pool"] = pool
            session["mode"] = mode
            session["idx"] = 0
            session["score"] = 0
            session["wrong"] = []
            session["times"] = []
            session["start_time"] = time.time()
            session["result"] = ""  # 정답/오답 결과 메시지 저장용
            session["step"] = "quiz"
            
            return redirect(url_for("home"))

        # 3. 퀴즈 정답 제출 시 처리
        if "answer" in request.form and session["step"] == "quiz":
            pool = session.get("pool", [])
            idx = session.get("idx", 0)

            if idx < len(pool):
                word = pool[idx]
                # 모드에 따른 정답 설정
                answer = word[0] if session["mode"] == "1" else word[1]
                
                # 시간 측정
                now = time.time()
                session["times"].append(now - session["start_time"])
                session["start_time"] = now  # 다음 문제를 위한 시간 리셋

                user_ans = request.form["answer"].strip().lower()
                real_ans = answer.strip().lower()

                if user_ans == real_ans:
                    session["score"] += 2
                    session["result"] = f"⭕ 정답입니다!"
                else:
                    session["wrong"].append(word)
                    session["result"] = f"❌ 오답! 정답은 [{answer}] 입니다."

                # 정답 확인 후 확실하게 인덱스를 증가시킴
                session["idx"] += 1
                
                # 50문제를 다 풀었으면 종료 단계로 전환
                if session["idx"] >= 50:
                    session["step"] = "end"

            return redirect(url_for("home"))

    # =========================
    # GET 요청 처리 (화면 그려주기)
    # =========================
    if session["step"] == "start":
        return render_template_string(HTML, step="start")

    elif session["step"] == "quiz":
        pool = session.get("pool", [])
        idx = session.get("idx", 0)

        # 예외 처리: 인덱스가 범위를 벗어나면 바로 결과창으로
        if idx >= len(pool):
            session["step"] = "end"
            return redirect(url_for("home"))

        word = pool[idx]
        question = word[1] if session["mode"] == "1" else word[0]
        answer = word[0] if session["mode"] == "1" else word[1]
        hint = len(answer)

        return render_template_string(
            HTML,
            step="quiz",
            score=session["score"],
            idx=idx + 1,  # 사용자 화면에는 1번 문제부터 표시되도록 변경
            question=question,
            hint=hint,
            result=session.get("result", "")
        )

    elif session["step"] == "end":
        score = session.get("score", 0)
        # 50문제 만점이므로 정답률 계산 (점수 기준이 아닌 문제 수 기준으로 조정 가능)
        acc = round((score / 100) * 100, 2)
        times = session.get("times", [])
        avg = sum(times) / len(times) if times else 0

        return render_template_string(
            HTML,
            step="end",
            score=score,
            acc=acc,
            g=grade(acc),
            avg=round(avg, 2),
            wrong=session.get("wrong", [])
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
