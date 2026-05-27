    import { useState, useEffect } from "react";
    import "./Blacklist.css";

    const INDUSTRIES = ["전체", "IT/전자", "컨설팅", "스타트업", "금융", "제조"];
    const BASE_URL = "http://localhost:8000";

    export default function Blacklist() {
    const [reviews, setReviews] = useState([]);
    const [companies, setCompanies] = useState([]);
    const [currentUser, setCurrentUser] = useState(null); // 내 정보 저장용
    const [filter, setFilter] = useState("전체");
    const [search, setSearch] = useState("");
    const [showForm, setShowForm] = useState(false);
    const [form, setForm] = useState({ company_name: "", title: "", content: "" });
    const [isLoading, setIsLoading] = useState(true);
    const [errors, setErrors] = useState({});
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
        try {
            const token = localStorage.getItem("accessToken");
            
            // 1. 내 정보 가져오기 (삭제 버튼 표시 권한 확인용)
            if (token) {
            try {
                const userRes = await fetch(`${BASE_URL}/auth/me`, {
                headers: { Authorization: `Bearer ${token}` }
                });
                if (userRes.ok) {
                const userData = await userRes.json();
                setCurrentUser(userData);
                }
            } catch (e) { console.error("내 정보 로딩 실패"); }
            }

            // 2. 회사 및 리뷰 목록 가져오기
            const res = await fetch(`${BASE_URL}/companies`);
            if (!res.ok) throw new Error("회사 목록 로딩 실패");
            const companyList = await res.json();
            setCompanies(companyList);

            const allReviews = [];
            await Promise.all(
            companyList.map(async (company) => {
                try {
                const rRes = await fetch(`${BASE_URL}/companies/${company.id}/reviews`);
                if (!rRes.ok) return;
                const rData = await rRes.json();
                rData.forEach((r) =>
                    allReviews.push({
                    ...r,
                    company_name: company.company_name,
                    industry: company.industry || "기타",
                    })
                );
                } catch (_) {}
            })
            );
            setReviews(allReviews.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)));
        } catch (e) {
            console.error(e);
        } finally {
            setIsLoading(false);
        }
        };
        fetchData();
    }, []);

    const filtered = reviews.filter((r) => {
        const matchFilter = filter === "전체" || r.industry === filter;
        const matchSearch =
        !search || 
        r.company_name?.toLowerCase().includes(search.toLowerCase()) || 
        r.content?.toLowerCase().includes(search.toLowerCase());
        return matchFilter && matchSearch;
    });

    function openModal() {
        const token = localStorage.getItem("accessToken");
        if (!token) {
        alert("로그인이 필요합니다.");
        return;
        }
        setShowForm(true);
    }

    function closeModal() {
        setShowForm(false);
        setForm({ company_name: "", title: "", content: "" });
        setErrors({});
    }

    // 💡 삭제 로직
    async function handleDelete(reviewId) {
        if (!window.confirm("정말 이 리뷰를 삭제하시겠습니까?")) return;
        
        const token = localStorage.getItem("accessToken");
        try {
        const res = await fetch(`${BASE_URL}/companies/reviews/${reviewId}`, {
            method: "DELETE",
            headers: { Authorization: `Bearer ${token}` }
        });
        if (res.ok) {
            setReviews(reviews.filter(r => r.id !== reviewId));
            alert("삭제되었습니다.");
        } else {
            alert("삭제 권한이 없거나 이미 삭제된 리뷰입니다.");
        }
        } catch (e) {
        alert("서버 통신 오류가 발생했습니다.");
        }
    }

    async function handleSubmit() {
        const newErrors = {};
        if (!form.company_name.trim()) newErrors.company_name = "회사명을 입력해주세요.";
        if (!form.content.trim()) newErrors.content = "내용을 입력해주세요.";
        
        if (Object.keys(newErrors).length > 0) {
        setErrors(newErrors);
        return;
        }

        const token = localStorage.getItem("accessToken");
        setSubmitting(true);

        try {
        // 💡 바뀐 수기 입력 엔드포인트 사용
        const res = await fetch(`${BASE_URL}/companies/manual/reviews`, {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
            company_name: form.company_name.trim(),
            is_anonymous: true,
            content: form.content,
            resignation_reason: form.title,
            }),
        });

        if (res.ok) {
            const newReview = await res.json();
            // 등록 후 즉시 리스트에 추가 (디자인 유지)
            setReviews((prev) => [
            {
                ...newReview,
                company_name: form.company_name.trim(),
                industry: "기타",
            },
            ...prev,
            ]);
            closeModal();
        } else {
            const err = await res.json().catch(() => ({}));
            alert(err.detail || "리뷰 등록에 실패했습니다.");
        }
        } catch (e) {
        alert("서버 연결에 실패했습니다.");
        } finally {
        setSubmitting(false);
        }
    }

    return (
        <div className="bl-root">
        <div className="bl-header">
            <div className="bl-header-inner">
            <div>
                <div className="bl-badge">블랙리스트</div>
                <h1 className="bl-title">피해야 할 회사 리뷰</h1>
                <p className="bl-subtitle">선배들의 솔직한 경험담. 지원 전에 꼭 확인하세요.</p>
            </div>
            <button className="bl-write-btn" onClick={openModal}>
                ✏️ 리뷰 작성
            </button>
            </div>

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

        <div className="bl-body">
            {isLoading ? (
            <div className="bl-empty">
                <p className="bl-empty-text">불러오는 중...</p>
            </div>
            ) : filtered.length === 0 ? (
            <div className="bl-empty">
                <div className="bl-empty-icon">🔍</div>
                <p className="bl-empty-text">검색 결과가 없어요.</p>
            </div>
            ) : (
            <div className="bl-list">
                {filtered.map((r) => {
                // 별점 계산 로직 유지
                const score = r.work_life_balance_score
                    ? Math.round(r.work_life_balance_score)
                    : 0;
                return (
                    <div key={r.id} className="bl-card">
                    <div className="bl-card-top">
                        <div className="bl-card-meta">
                        <span className="bl-card-company">{r.company_name}</span>
                        <span className="bl-card-industry">{r.industry}</span>
                        </div>
                        <div className="bl-card-stars">
                        {"★".repeat(score) + "☆".repeat(5 - score)}
                        </div>
                    </div>
                    <h3 className="bl-card-title">{r.resignation_reason || "솔직한 후기"}</h3>
                    <p className="bl-card-content">{r.content}</p>
                    <div className="bl-card-footer">
                        <div className="bl-card-info">
                        {r.is_anonymous ? "익명" : "작성자"} ·{" "}
                        {new Date(r.created_at).toLocaleDateString("ko-KR")}
                        </div>
                        {/* 💡 삭제 버튼 추가: 내 글일 때만 노출 */}
                        {currentUser && r.user_id === currentUser.id && (
                        <button 
                            className="bl-delete-link" 
                            onClick={() => handleDelete(r.id)}
                            style={{
                            color: '#e11d48',
                            background: 'none',
                            border: 'none',
                            fontSize: '12px',
                            fontWeight: '600',
                            cursor: 'pointer',
                            textDecoration: 'underline'
                            }}
                        >
                            삭제하기
                        </button>
                        )}
                    </div>
                    </div>
                );
                })}
            </div>
            )}
        </div>

        {showForm && (
            <>
            <div className="bl-overlay" onClick={closeModal} />
            <div className="bl-modal">
                <div className="bl-modal-header">
                <h2 className="bl-modal-title">리뷰 작성</h2>
                <button className="bl-modal-close" onClick={closeModal}>✕</button>
                </div>
                <div className="bl-modal-body">
                <div className="bl-field">
                    <label className="bl-label">회사 이름 *</label>
                    <input
                    className={`bl-input ${errors.company_name ? 'error' : ''}`}
                    placeholder="회사명을 직접 입력하세요"
                    value={form.company_name}
                    onChange={(e) => setForm({ ...form, company_name: e.target.value })}
                    />
                    {errors.company_name && <p className="bl-error">{errors.company_name}</p>}
                </div>

                <div className="bl-field">
                    <label className="bl-label">한 줄 요약 (제목)</label>
                    <input
                    className="bl-input"
                    placeholder="예: 최악의 워라밸, 임금 체불 등"
                    value={form.title}
                    onChange={(e) => setForm({ ...form, title: e.target.value })}
                    />
                </div>

                <div className="bl-field">
                    <label className="bl-label">리뷰 내용 *</label>
                    <textarea
                    className={`bl-textarea ${errors.content ? 'error' : ''}`}
                    placeholder="솔직한 경험을 공유해주세요 (익명성이 보장됩니다)"
                    value={form.content}
                    onChange={(e) => setForm({ ...form, content: e.target.value })}
                    />
                    {errors.content && <p className="bl-error">{errors.content}</p>}
                </div>
                </div>
                <div className="bl-modal-footer">
                <button className="bl-cancel-btn" onClick={closeModal}>취소</button>
                <button
                    className="bl-submit-btn"
                    onClick={handleSubmit}
                    disabled={submitting}
                >
                    {submitting ? "등록 중..." : "익명으로 등록"}
                </button>
                </div>
            </div>
            </>
        )}
        </div>
    );
    }