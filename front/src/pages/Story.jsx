    import { useState } from "react";
    import "./Story.css";

    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // ✏️  여기에 스토리와 선택지를 채워넣으세요
    //
    // 각 항목 구조:
    //   id      : 문항 순서 번호 (숫자)
    //   scene   : 상단에 표시되는 장면 라벨 (예: "1화", "에피소드 1" 등)
    //   story   : 📖 스토리 본문 — 여러 단락을 배열로 작성
    //             (줄바꿈 단락마다 별도 문자열로 넣으면 단락 구분됩니다)
    //   question: 스토리 아래 표시되는 선택 질문
    //   options : A/B 두 선택지
    //     ├ label : "A" 또는 "B" (고정)
    //     ├ text  : 버튼 메인 텍스트 (\n으로 줄바꿈 가능)
    //     ├ sub   : 버튼 보조 설명 (짧게)
    //     └ tag   : 결과 계산용 키값 (영문, 중복 가능)
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    const QUESTIONS = [
    {
        id: 1,
        scene: "상황 1",
        story: [
        "스토리 첫 번째 단락을 여기에 작성해주세요.",
        "두 번째 단락은 이렇게 이어서 씁니다. 여러 단락을 배열로 추가할수록 글이 자연스럽게 이어집니다.",
        ],
        question: "✏️ 첫 번째 선택 질문을 여기에 작성해주세요.",
        options: [
        { label: "A", text: "✏️ A 선택지\n텍스트", sub: "✏️ A 보조 설명", tag: "solo" },
        { label: "B", text: "✏️ B 선택지\n텍스트", sub: "✏️ B 보조 설명", tag: "team" },
        ],
    },
    {
        id: 2,
        scene: "이어진 상황 2",
        story: [
        "✏️ 두 번째 스토리 첫 번째 단락.",
        "두 번째 단락을 이어서 씁니다.",
        ],
        question: "✏️ 두 번째 선택 질문을 여기에 작성해주세요.",
        options: [
        { label: "A", text: "✏️ A 선택지\n텍스트", sub: "✏️ A 보조 설명", tag: "stable" },
        { label: "B", text: "✏️ B 선택지\n텍스트", sub: "✏️ B 보조 설명", tag: "dynamic" },
        ],
    },
    {
        id: 3,
        scene: "이어진 상황 3",
        story: [
        "✏️ 세 번째 스토리 첫 번째 단락.",
        "두 번째 단락을 이어서 씁니다.",
        ],
        question: "✏️ 세 번째 선택 질문을 여기에 작성해주세요.",
        options: [
        { label: "A", text: "✏️ A 선택지\n텍스트", sub: "✏️ A 보조 설명", tag: "creative" },
        { label: "B", text: "✏️ B 선택지\n텍스트", sub: "✏️ B 보조 설명", tag: "analytical" },
        ],
    },
    {
        id: 4,
        scene: "이어진 상황 4",
        story: [
        "✏️ 네 번째 스토리 첫 번째 단락.",
        "두 번째 단락을 이어서 씁니다.",
        ],
        question: "✏️ 네 번째 선택 질문을 여기에 작성해주세요.",
        options: [
        { label: "A", text: "✏️ A 선택지\n텍스트", sub: "✏️ A 보조 설명", tag: "employed" },
        { label: "B", text: "✏️ B 선택지\n텍스트", sub: "✏️ B 보조 설명", tag: "independent" },
        ],
    },
    {
        id: 5,
        scene: "이어진 상황 5",
        story: [
        "✏️ 다섯 번째 스토리 첫 번째 단락.",
        "두 번째 단락을 이어서 씁니다.",
        ],
        question: "✏️ 다섯 번째 선택 질문을 여기에 작성해주세요.",
        options: [
        { label: "A", text: "✏️ A 선택지\n텍스트", sub: "✏️ A 보조 설명", tag: "people" },
        { label: "B", text: "✏️ B 선택지\n텍스트", sub: "✏️ B 보조 설명", tag: "tech" },
        ],
    },
    ];

    const RESULTS = [
    {
        type: "크리에이티브 디렉터",
        emoji: "🎨",
        color: "#7c3aed",
        bg: "#f5f3ff",
        border: "#ddd6fe",
        match: (t) => t.creative >= 1 && t.dynamic >= 1,
        desc: "당신은 새로운 것을 만드는 데 탁월한 감각을 가졌어요. 콘텐츠 크리에이터, UX 디자이너, 브랜드 기획자 등 창의성을 살릴 수 있는 직군이 최고의 선택!",
        jobs: ["UX/UI 디자이너", "브랜드 기획자", "콘텐츠 크리에이터", "광고 PD"],
        tip: "포트폴리오를 꾸준히 쌓아가세요. 나만의 작업물이 최고의 명함입니다.",
    },
    {
        type: "데이터 전문가",
        emoji: "📈",
        color: "#0369a1",
        bg: "#f0f9ff",
        border: "#bae6fd",
        match: (t) => t.analytical >= 1 && t.solo >= 1,
        desc: "논리와 수치로 세상을 보는 당신. 데이터 분석가, 개발자, 퀀트 애널리스트처럼 정밀함이 무기인 직업이 딱 맞아요.",
        jobs: ["데이터 애널리스트", "백엔드 개발자", "금융 분석가", "리서처"],
        tip: "SQL, Python 등 분석 툴을 익혀두면 어느 산업에서도 환영받아요.",
    },
    {
        type: "비즈니스 컨설턴트",
        emoji: "🧭",
        color: "#0f766e",
        bg: "#f0fdfa",
        border: "#99f6e4",
        match: (t) => t.team >= 1 && t.analytical >= 1,
        desc: "전략적 사고와 팀워크를 겸비한 리더형! 컨설팅, 전략기획, PM처럼 비즈니스를 조율하는 역할이 천직이에요.",
        jobs: ["경영 컨설턴트", "전략기획자", "프로덕트 매니저", "MBA 진학"],
        tip: "다양한 산업을 경험하고 인맥을 넓히는 게 핵심 경쟁력입니다.",
    },
    {
        type: "소셜 임팩트 전문가",
        emoji: "🌱",
        color: "#15803d",
        bg: "#f0fdf4",
        border: "#bbf7d0",
        match: (t) => t.people >= 1 && t.team >= 1,
        desc: "사람과 사회에 기여하는 일에서 에너지를 얻는 타입. 교육, 사회복지, NGO, 의료 분야에서 진정한 보람을 찾을 거예요.",
        jobs: ["사회복지사", "교육기획자", "NPO 활동가", "상담사"],
        tip: "현장 경험이 강점입니다. 자원봉사와 인턴으로 먼저 뛰어들어보세요.",
    },
    {
        type: "스타트업 창업가",
        emoji: "🚀",
        color: "#b45309",
        bg: "#fffbeb",
        border: "#fde68a",
        match: (t) => t.independent >= 1 && t.dynamic >= 1,
        desc: "틀을 깨고 나만의 길을 만드는 개척자! 스타트업 창업, 프리랜서, 1인 기업가로서 독립적인 커리어를 만들어갈 당신이에요.",
        jobs: ["스타트업 창업가", "프리랜서", "유튜버·인플루언서", "디지털 노마드"],
        tip: "빠른 실행과 실패 경험이 자산입니다. 지금 당장 작은 것부터 시작해보세요.",
    },
    {
        type: "IT 이노베이터",
        emoji: "⚡",
        color: "#7c3aed",
        bg: "#faf5ff",
        border: "#e9d5ff",
        match: (t) => t.tech >= 1 && (t.dynamic >= 1 || t.analytical >= 1),
        desc: "기술로 세상을 바꾸고 싶은 당신! 개발자, AI 엔지니어, 테크 PM처럼 미래를 설계하는 직군이 잘 맞아요.",
        jobs: ["소프트웨어 엔지니어", "AI/ML 엔지니어", "DevOps", "테크 스타트업 합류"],
        tip: "깃헙 잔디를 채우며 꾸준히 성장하세요. 기술은 배신하지 않아요.",
    },
    ];

    // ⚠️ 나중에 이 함수를 AI API 호출로 교체하면 됩니다
    function getResult(answers) {
    const tags = {};
    answers.forEach((a) => { tags[a] = (tags[a] || 0) + 1; });
    for (const r of RESULTS) {
        if (r.match(tags)) return r;
    }
    return RESULTS[Math.floor(Math.random() * RESULTS.length)];
    }

    export default function Story() {
    const [phase, setPhase] = useState("intro");
    const [step, setStep] = useState(0);
    const [answers, setAnswers] = useState([]);
    const [selected, setSelected] = useState(null);
    const [result, setResult] = useState(null);
    const [animKey, setAnimKey] = useState(0);

    function startGame() {
        setPhase("game");
        setStep(0);
        setAnswers([]);
        setSelected(null);
        setAnimKey((k) => k + 1);
    }

    function handleSelect(tag) {
        if (selected !== null) return;
        setSelected(tag);
        setTimeout(() => {
        const next = [...answers, tag];
        if (step + 1 >= QUESTIONS.length) {
            setResult(getResult(next));
            setPhase("result");
        } else {
            setAnswers(next);
            setStep((s) => s + 1);
            setSelected(null);
            setAnimKey((k) => k + 1);
        }
        }, 480);
    }

    function restart() {
        setPhase("intro");
        setStep(0);
        setAnswers([]);
        setSelected(null);
        setResult(null);
    }

    const progress = (step / QUESTIONS.length) * 100;
    const q = QUESTIONS[step];

    return (
        <div className="story-root">

        {/* ─── INTRO ─── */}
        {phase === "intro" && (
            <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "40px 24px", textAlign: "center" }}>
            <div className="anim-fadeup" style={{ maxWidth: 520 }}>
                <div style={{ display: "inline-block", background: "#f1effe", color: "#7c3aed", borderRadius: "100px", padding: "8px 20px", fontSize: 13, fontWeight: 700, letterSpacing: "0.08em", marginBottom: 28 }}>
                ✦ 스토리형 밸런스 게임
                </div>
                <h1 style={{ fontSize: "clamp(32px, 6vw, 52px)", fontWeight: 900, color: "#1c1917", lineHeight: 1.15, marginBottom: 20 }}>
                나에게 맞는<br />
                <span style={{ color: "#7c3aed" }}>진로</span>는 뭘까?
                </h1>
                <p style={{ fontSize: 17, color: "#78716c", lineHeight: 1.75, marginBottom: 48 }}>
                나에게 딱 맞는 커리어를 알려드려요.
                </p>
                <div style={{ display: "flex", gap: 10, justifyContent: "center", marginBottom: 48 }}>
                {["업무 방식", "성장 방향", "가치관"].map((t, i) => (
                    <div key={i} style={{ background: "#fff", border: "1.5px solid #e5e2dc", borderRadius: 14, padding: "10px 18px", fontSize: 13, fontWeight: 500, color: "#57534e" }}>
                    {t}
                    </div>
                ))}
                </div>
                <button className="start-btn" onClick={startGame}>
                <span>게임 시작하기</span>
                <span style={{ fontSize: 20 }}>→</span>
                </button>
            </div>
            </div>
        )}

        {/* ─── GAME ─── */}
        {phase === "game" && (
            <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column", alignItems: "center", padding: "0 24px 60px" }}>

            {/* Top bar */}
            <div style={{ width: "100%", maxWidth: 580, paddingTop: 32 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
                <span style={{ fontSize: 13, color: "#a8a29e", fontWeight: 500 }}>
                    {step + 1} / {QUESTIONS.length}
                </span>
                <button onClick={restart} style={{ background: "none", border: "none", fontSize: 13, color: "#a8a29e", cursor: "pointer", padding: "4px 8px" }}>
                    ✕ 처음으로
                </button>
                </div>
                <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${progress}%` }} />
                </div>
            </div>

            {/* Question card */}
            <div key={animKey} className="anim-fadeup" style={{ width: "100%", maxWidth: 580, marginTop: 48 }}>

                {/* Scene badge */}
                <div style={{ fontSize: 13, fontWeight: 700, color: "#7c3aed", letterSpacing: "0.06em", marginBottom: 16 }}>
                {q.scene}
                </div>

                {/* 스토리 본문 */}
                <div style={{ background: "#fff", border: "1.5px solid #e5e2dc", borderLeft: "4px solid #7c3aed", borderRadius: "0 20px 20px 0", padding: "24px 28px", marginBottom: 32 }}>
                {q.story.map((paragraph, i) => (
                    <p key={i} style={{ margin: i === 0 ? 0 : "14px 0 0", fontSize: 15, color: "#3d3935", lineHeight: 1.85, letterSpacing: "0.01em" }}>
                    {paragraph}
                    </p>
                ))}
                </div>

                {/* Question */}
                <h2 style={{ fontSize: "clamp(18px, 4vw, 24px)", fontWeight: 900, color: "#1c1917", marginBottom: 20, lineHeight: 1.3, padding: "0 2px" }}>
                {q.question}
                </h2>

                {/* Options */}
                <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                {q.options.map((opt) => (
                    <button
                    key={opt.label}
                    className={`story-btn${selected === opt.tag ? " selected" : ""}`}
                    onClick={() => handleSelect(opt.tag)}
                    style={{ opacity: selected && selected !== opt.tag ? 0.45 : 1 }}
                    >
                    <div className="label-badge">{opt.label}</div>
                    <div style={{ flex: 1 }}>
                        <div style={{ fontSize: "clamp(15px, 3vw, 17px)", fontWeight: 700, color: "#1c1917", whiteSpace: "pre-line", lineHeight: 1.4, marginBottom: 6 }}>
                        {opt.text}
                        </div>
                        <div style={{ fontSize: 13, color: "#a8a29e" }}>{opt.sub}</div>
                    </div>
                    {selected === opt.tag && (
                        <div style={{ position: "absolute", right: 20, top: "50%", transform: "translateY(-50%)", width: 28, height: 28, borderRadius: "50%", background: "#7c3aed", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontSize: 14, animation: "pop 0.3s ease both" }}>
                        ✓
                        </div>
                    )}
                    </button>
                ))}
                </div>

                <div style={{ textAlign: "center", marginTop: 20, fontSize: 12, color: "#c4bfb8" }}>
                본능대로 고르세요
                </div>
            </div>
            </div>
        )}

        {/* ─── RESULT ─── */}
        {phase === "result" && result && (
            <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column", alignItems: "center", padding: "48px 24px 80px" }}>
            <div className="anim-fadeup" style={{ width: "100%", maxWidth: 580 }}>

                {/* Result header */}
                <div style={{ textAlign: "center", marginBottom: 36 }}>
                <div style={{ fontSize: 72, marginBottom: 12, lineHeight: 1, animation: "pulse 2s ease infinite", display: "inline-block" }}>
                    {result.emoji}
                </div>
                <div style={{ display: "inline-block", background: result.bg, color: result.color, borderRadius: "100px", padding: "6px 18px", fontSize: 13, fontWeight: 700, marginBottom: 16 }}>
                    당신에게 어울리는 커리어
                </div>
                <h1 style={{ fontSize: "clamp(28px, 6vw, 42px)", fontWeight: 900, color: "#1c1917", marginBottom: 8 }}>
                    {result.type}
                </h1>
                </div>

                {/* Description */}
                <div style={{ background: result.bg, border: `2px solid ${result.border}`, borderRadius: 24, padding: "28px 28px", marginBottom: 24 }}>
                <p style={{ margin: 0, fontSize: 16, color: "#44403c", lineHeight: 1.75 }}>{result.desc}</p>
                </div>

                {/* Recommended jobs */}
                <div style={{ background: "#fff", border: "1.5px solid #e5e2dc", borderRadius: 20, padding: "24px 28px", marginBottom: 24 }}>
                <div style={{ fontSize: 12, fontWeight: 700, color: "#a8a29e", letterSpacing: "0.1em", marginBottom: 16 }}>
                    추천 직군 · 직무
                </div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
                    {result.jobs.map((job) => (
                    <span key={job} className="job-chip">{job}</span>
                    ))}
                </div>
                </div>

                {/* Tip */}
                <div style={{ background: "#1c1917", borderRadius: 20, padding: "22px 28px", marginBottom: 40, display: "flex", gap: 16, alignItems: "flex-start" }}>
                <span style={{ fontSize: 22, flexShrink: 0 }}>💡</span>
                <div>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#a78bfa", letterSpacing: "0.1em", marginBottom: 6 }}>커리어 팁</div>
                    <p style={{ margin: 0, fontSize: 15, color: "#e7e5e0", lineHeight: 1.65 }}>{result.tip}</p>
                </div>
                </div>

                {/* Buttons */}
                <div style={{ display: "flex", gap: 12, justifyContent: "center", flexWrap: "wrap" }}>
                <button className="start-btn" onClick={startGame}>
                    <span>다시 해보기</span>
                    <span>↺</span>
                </button>
                <button className="restart-btn" onClick={restart}>
                    <span>처음으로</span>
                </button>
                </div>
            </div>
            </div>
        )}
        </div>
    );
    }