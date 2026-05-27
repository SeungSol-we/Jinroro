    import { useState, useEffect } from "react";
    import { useNavigate } from "react-router-dom";
    import "./MyPage.css";

    const MyPage = () => {
    const navigate = useNavigate();
    const [userInfo, setUserInfo] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchUser = async () => {
        const token = localStorage.getItem("accessToken");
        if (!token) { navigate("/login"); return; }

        try {
            const res = await fetch("http://localhost:8000/auth/me", {
            headers: { Authorization: `Bearer ${token}` },
            });
            if (!res.ok) { navigate("/login"); return; }
            const data = await res.json();
            setUserInfo(data);
        } catch (e) {
            console.error(e);
        } finally {
            setIsLoading(false);
        }
        };
        fetchUser();
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        navigate("/login");
    };

    const handleDeleteAccount = async () => {
        if (!window.confirm("정말 탈퇴하시겠어요? 모든 데이터가 삭제됩니다.")) return;
        const token = localStorage.getItem("accessToken");
        try {
        const res = await fetch("http://localhost:8000/auth/me", {
            method: "DELETE",
            headers: { Authorization: `Bearer ${token}` },
        });
        if (res.ok) {
            localStorage.removeItem("accessToken");
            localStorage.removeItem("refreshToken");
            alert("탈퇴가 완료되었습니다.");
            navigate("/login");
        } else {
            alert("탈퇴에 실패했습니다.");
        }
        } catch (e) {
        alert("오류가 발생했습니다.");
        }
    };

    if (isLoading) return <div className="mypage-loading">불러오는 중...</div>;

    return (
        <div className="mypage-root">
        <div className="mypage-container">
            <h1 className="mypage-title">마이페이지</h1>

            <section className="mypage-section">
            <h2 className="mypage-section-title">계정 정보</h2>
            <div className="mypage-info-card">
                <div className="mypage-info-row">
                <span className="mypage-info-label">이메일</span>
                <span className="mypage-info-value">{userInfo?.email}</span>
                </div>

            </div>
            </section>

            <section className="mypage-section">
            <h2 className="mypage-section-title">계정 관리</h2>
            <div className="mypage-action-card">
                <button className="mypage-delete-btn" onClick={handleDeleteAccount}>
                회원 탈퇴
                </button>
            </div>
            </section>
        </div>
        </div>
    );
    };

    export default MyPage;