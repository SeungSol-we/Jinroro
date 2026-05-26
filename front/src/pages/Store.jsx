    import { useState } from "react";
    import "./Store.css";

    // 임시 더미 데이터 — 나중에 백엔드 연결 시 교체
    const DUMMY_ITEMS = [
    { id: 1, tag: "solo", label: "혼자 일하기", desc: "팀 협업보다 혼자 집중하는 환경이 싫어요", date: "2026.05.20", category: "업무방식" },
    { id: 2, tag: "stable", label: "반복적인 루틴", desc: "매일 똑같은 업무가 반복되는 환경이 싫어요", date: "2026.05.20", category: "업무방식" },
    { id: 3, tag: "employed", label: "대기업 직장인", desc: "조직 안에서 정해진 역할만 하는 게 싫어요", date: "2026.05.19", category: "커리어방향" },
    ];

    const CATEGORY_COLORS = {
    "업무방식":   { bg: "#f5f3ff", color: "#7c3aed", border: "#ddd6fe" },
    "커리어방향": { bg: "#f0f9ff", color: "#0369a1", border: "#bae6fd" },
    "가치관":     { bg: "#f0fdf4", color: "#15803d", border: "#bbf7d0" },
    };

    export default function Store() {
    const [items, setItems] = useState(DUMMY_ITEMS);
    const [filter, setFilter] = useState("전체");

    const categories = ["전체", ...new Set(DUMMY_ITEMS.map((i) => i.category))];
    const filtered = filter === "전체" ? items : items.filter((i) => i.category === filter);

    function remove(id) {
        setItems((prev) => prev.filter((i) => i.id !== id));
    }

    return (
        <div className="store-root">
        {/* 헤더 영역 */}
        <div className="store-header">
            <div className="store-header-inner">
            <div>
                <div className="store-badge">🗂️ 싫음 보관함</div>
                <h1 className="store-title">내가 싫은 것들</h1>
                <p className="store-subtitle">탐색기에서 선택한 결과가 여기에 쌓여요.<br />나만의 진로 필터가 됩니다.</p>
            </div>
            <div className="store-count-box">
                <span className="store-count-num">{items.length}</span>
                <span className="store-count-label">개 저장됨</span>
            </div>
            </div>

            {/* 필터 탭 */}
            <div className="store-filters">
            {categories.map((c) => (
                <button
                key={c}
                className={`store-filter-btn${filter === c ? " active" : ""}`}
                onClick={() => setFilter(c)}
                >
                {c}
                </button>
            ))}
            </div>
        </div>

        {/* 카드 목록 */}
        <div className="store-body">
            {filtered.length === 0 ? (
            <div className="store-empty">
                <div className="store-empty-icon">🤔</div>
                <p className="store-empty-text">아직 저장된 항목이 없어요.<br />싫음 탐색기를 먼저 해보세요!</p>
            </div>
            ) : (
            <div className="store-grid">
                {filtered.map((item) => {
                const col = CATEGORY_COLORS[item.category] || CATEGORY_COLORS["가치관"];
                return (
                    <div key={item.id} className="store-card">
                    <div className="store-card-top">
                        <span className="store-card-category" style={{ background: col.bg, color: col.color, border: `1.5px solid ${col.border}` }}>
                        {item.category}
                        </span>
                        <button className="store-card-remove" onClick={() => remove(item.id)}>✕</button>
                    </div>
                    <div className="store-card-label">{item.label}</div>
                    <div className="store-card-desc">{item.desc}</div>
                    <div className="store-card-date">{item.date}</div>
                    </div>
                );
                })}
            </div>
            )}
        </div>
        </div>
    );
    }