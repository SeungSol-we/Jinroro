    import { useState } from "react";
    import "./Blacklist.css";

    const DUMMY_REVIEWS = [
    {
        id: 1, company: "○○전자", industry: "IT/전자", rating: 1,
        title: "야근이 일상인 회사",
        content: "퇴근 시간이 따로 없어요. 팀장이 눈치를 줘서 아무도 못 나가고, 주말에도 카톡이 옵니다. 신입은 그냥 소모품 취급.",
        tags: ["야근", "수직문화", "소통불가"],
        author: "익명", date: "2026.05.18", likes: 34,
    },
    {
        id: 2, company: "△△컨설팅", industry: "컨설팅", rating: 1,
        title: "면접관부터 무례했던 곳",
        content: "면접에서 개인 SNS를 왜 보냈냐고 따지더니, 연봉 협상도 일방적으로 통보. 입사 전부터 이러면 입사 후는 어떨지...",
        tags: ["갑질", "연봉후려치기", "비추천"],
        author: "익명", date: "2026.05.15", likes: 21,
    },
    {
        id: 3, company: "□□스타트업", industry: "스타트업", rating: 2,
        title: "스타트업이라는 말로 모든 걸 합리화",
        content: "스타트업 특성상 다 해야 한다며 직무 외 잡무가 끝이 없음. 스톡옵션 얘기로 꼬드기는데 실현 가능성 0.",
        tags: ["다직무강요", "스톡옵션사기", "번아웃"],
        author: "익명", date: "2026.05.10", likes: 18,
    },
    ];

    const INDUSTRIES = ["전체", "IT/전자", "컨설팅", "스타트업", "금융", "제조"];

    export default function Blacklist() {
    const [reviews, setReviews] = useState(DUMMY_REVIEWS);
    const [filter, setFilter] = useState("전체");
    const [search, setSearch] = useState("");
    const [showForm, setShowForm] = useState(false);
    const [form, setForm] = useState({ company: "", industry: "IT/전자", title: "", content: "", tags: "" });

    const filtered = reviews.filter((r) => {
        const matchFilter = filter === "전체" || r.industry === filter;
        const matchSearch = r.company.includes(search) || r.title.includes(search);
        return matchFilter && matchSearch;
    });

    function handleLike(id) {
        setReviews((prev) => prev.map((r) => r.id === id ? { ...r, likes: r.likes + 1 } : r));
    }

    function handleSubmit() {
        if (!form.company || !form.title || !form.content) return;
        const newReview = {
        id: Date.now(),
        company: form.company,
        industry: form.industry,
        rating: 1,
        title: form.title,
        content: form.content,
        tags: form.tags.split(",").map((t) => t.trim()).filter(Boolean),
        author: "익명",
        date: new Date().toLocaleDateString("ko-KR").replace(/\. /g, ".").replace(".", "").slice(0, -1),
        likes: 0,
        };
        setReviews((prev) => [newReview, ...prev]);
        setForm({ company: "", industry: "IT/전자", title: "", content: "", tags: "" });
        setShowForm(false);
    }

    return (
        <div className="bl-root">
        {/* 헤더 */}
        <div className="bl-header">
            <div className="bl-header-inner">
            <div>
                <div className="bl-badge">🚫 블랙리스트</div>
                <h1 className="bl-title">피해야 할 회사 리뷰</h1>
                <p className="bl-subtitle">선배들의 솔직한 경험담. 지원 전에 꼭 확인하세요.</p>
            </div>
            <button className="bl-write-btn" onClick={() => setShowForm(true)}>
                ✏️ 리뷰 작성
            </button>
            </div>

            {/* 검색 + 필터 */}
            <div className="bl-controls">
            <div className="bl-search-wrap">
                <span className="bl-search-icon">🔍</span>
                <input
                className="bl-search"
                placeholder="회사명 또는 키워드 검색"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                />
            </div>
            <div className="bl-filters">
                {INDUSTRIES.map((ind) => (
                <button
                    key={ind}
                    className={`bl-filter-btn${filter === ind ? " active" : ""}`}
                    onClick={() => setFilter(ind)}
                >
                    {ind}
                </button>
                ))}
            </div>
            </div>
        </div>

        {/* 리뷰 목록 */}
        <div className="bl-body">
            {filtered.length === 0 ? (
            <div className="bl-empty">
                <div className="bl-empty-icon">🔍</div>
                <p className="bl-empty-text">검색 결과가 없어요.</p>
            </div>
            ) : (
            <div className="bl-list">
                {filtered.map((r) => (
                <div key={r.id} className="bl-card">
                    <div className="bl-card-top">
                    <div className="bl-card-meta">
                        <span className="bl-card-company">{r.company}</span>
                        <span className="bl-card-industry">{r.industry}</span>
                    </div>
                    <div className="bl-card-stars">
                        {"★".repeat(r.rating)}{"☆".repeat(5 - r.rating)}
                    </div>
                    </div>
                    <h3 className="bl-card-title">{r.title}</h3>
                    <p className="bl-card-content">{r.content}</p>
                    <div className="bl-card-tags">
                    {r.tags.map((tag) => (
                        <span key={tag} className="bl-tag">#{tag}</span>
                    ))}
                    </div>
                    <div className="bl-card-footer">
                    <span className="bl-card-info">{r.author} · {r.date}</span>
                    <button className="bl-like-btn" onClick={() => handleLike(r.id)}>
                        👍 도움됐어요 {r.likes}
                    </button>
                    </div>
                </div>
                ))}
            </div>
            )}
        </div>

        {/* 리뷰 작성 모달 */}
        {showForm && (
            <>
            <div className="bl-overlay" onClick={() => setShowForm(false)} />
            <div className="bl-modal">
                <div className="bl-modal-header">
                <h2 className="bl-modal-title">리뷰 작성</h2>
                <button className="bl-modal-close" onClick={() => setShowForm(false)}>✕</button>
                </div>
                <div className="bl-modal-body">
                <div className="bl-field">
                    <label className="bl-label">회사명 *</label>
                    <input className="bl-input" placeholder="예: ○○전자" value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })} />
                </div>
                <div className="bl-field">
                    <label className="bl-label">업종</label>
                    <select className="bl-input" value={form.industry} onChange={(e) => setForm({ ...form, industry: e.target.value })}>
                    {INDUSTRIES.filter((i) => i !== "전체").map((i) => <option key={i}>{i}</option>)}
                    </select>
                </div>
                <div className="bl-field">
                    <label className="bl-label">제목 *</label>
                    <input className="bl-input" placeholder="한 줄로 요약해주세요" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
                </div>
                <div className="bl-field">
                    <label className="bl-label">내용 *</label>
                    <textarea className="bl-textarea" placeholder="솔직한 경험을 공유해주세요" value={form.content} onChange={(e) => setForm({ ...form, content: e.target.value })} />
                </div>
                <div className="bl-field">
                    <label className="bl-label">태그 (쉼표로 구분)</label>
                    <input className="bl-input" placeholder="예: 야근, 갑질, 비추천" value={form.tags} onChange={(e) => setForm({ ...form, tags: e.target.value })} />
                </div>
                </div>
                <div className="bl-modal-footer">
                <button className="bl-cancel-btn" onClick={() => setShowForm(false)}>취소</button>
                <button className="bl-submit-btn" onClick={handleSubmit}>익명으로 등록</button>
                </div>
            </div>
            </>
        )}
        </div>
    );
    }