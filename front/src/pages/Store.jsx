    import { useState } from "react";
    import "./Store.css";

    export default function Store() {
    // 현재 탭 상태 관리 (키워드, 분석, 휴지통)
    const [activeTab, setActiveTab] = useState("keyword");
    // 이미지와 동일한 상태를 위해 빈 배열로 설정
    const [items] = useState([]);

    return (
        <div className="store-root">
        {/* 기존 네비게이션 바는 상단에 이미 있다고 가정하고 본문부터 시작합니다 */}
        
        <main className="store-container anim-fadeup">
            {/* 타이틀 섹션 */}
            <div className="store-header-text">
            <h1 className="store-main-title">싫음 보관함</h1>
            <p className="store-main-subtitle">
                당신이 선택한 키워드들을 관리하고 분석해보세요.
            </p>
            </div>

            {/* 이미지와 동일한 알약 형태의 탭 메뉴 */}
            <div className="store-tabs-wrapper">
            <div className="store-tabs-bar">
                <button 
                className={`tab-btn ${activeTab === "keyword" ? "active" : ""}`}
                onClick={() => setActiveTab("keyword")}
                >
                키워드 ({items.length})
                </button>
                <button 
                className={`tab-btn ${activeTab === "analysis" ? "active" : ""}`}
                onClick={() => setActiveTab("analysis")}
                >
                분석
                </button>
                <button 
                className={`tab-btn ${activeTab === "trash" ? "active" : ""}`}
                onClick={() => setActiveTab("trash")}
                >
                휴지통 (0)
                </button>
            </div>
            </div>

            {/* 중앙 콘텐츠 영역 (Empty State) */}
            <section className="store-empty-content">
            <div className="empty-message-box anim-fadein">
                <p className="empty-msg-text">아직 키워드가 없어요</p>
                <button className="go-game-btn" onClick={() => window.location.href='/story'}>
                <span>게임 시작하기</span>
                </button>
            </div>
            </section>
        </main>

        </div>
    );
    }