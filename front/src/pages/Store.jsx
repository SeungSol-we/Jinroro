import { useState, useEffect } from "react";
import "./Store.css";

export default function Store() {
  const [activeTab, setActiveTab] = useState("keyword");
  
  // 상태 관리 리스트들
  const [keywords, setKeywords] = useState([]);
  const [trashItems, setTrashItems] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  
  const [isLoading, setIsLoading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const token = localStorage.getItem("accessToken");

  // 데이터 로드 스크립트
  const fetchStoreData = async () => {
    if (!token) return;
    setIsLoading(true);
    try {
      // 1. 활성화 보관함 키워드 조회
      const resActive = await fetch("http://localhost:8000/balance/avoid-tags", {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (resActive.ok) {
        const dataActive = await resActive.json();
        setKeywords(dataActive);
      }

      // 2. 휴지통 키워드 조회
      const resTrash = await fetch("http://localhost:8000/balance/trash-tags", {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (resTrash.ok) {
        const dataTrash = await resTrash.json();
        setTrashItems(dataTrash);
      }
    } catch (error) {
      console.error("데이터 로딩 오류:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchStoreData();
  }, []);

  // 🗑️ 보관함 키워드 -> 휴지통으로 이동 (Delete 요청)
  const handleDeleteKeyword = async (tagId) => {
    try {
      const response = await fetch(`http://localhost:8000/balance/avoid-tags/${tagId}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (response.ok) {
        alert("🗑️ 선택한 키워드가 휴지통으로 이동되었습니다.");
        fetchStoreData(); // 상태 갱신
      } else {
        alert("삭제에 실패했습니다.");
      }
    } catch (err) {
      console.error(err);
    }
  };

  // ↩️ 휴지통 키워드 -> 보관함으로 원복 (Restore 요청)
  const handleRestoreKeyword = async (tagId) => {
    try {
      const response = await fetch(`http://localhost:8000/balance/avoid-tags/${tagId}/restore`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (response.ok) {
        alert("🛡️ 키워드가 싫음 보관함으로 다시 복구되었습니다!");
        fetchStoreData();
      } else {
        alert("복구에 실패했습니다.");
      }
    } catch (err) {
      console.error(err);
    }
  };

  // 🤖 AI 불합치 직업 심층 분석 요청
  const handleRunAnalysis = async () => {
    setIsAnalyzing(true);
    try {
      const response = await fetch("http://localhost:8000/balance/analysis", {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (response.ok) {
        const result = await response.json();
        setAnalysis(result);
      } else {
        alert("AI 분석 결과를 가져오는 데 실패했습니다.");
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="store-root">
      <main className="store-container anim-fadeup">
        {/* 타이틀 섹션 */}
        <div className="store-header-text">
          <h1 className="store-main-title">싫음 보관함</h1>
          <p className="store-main-subtitle">
            당신이 가공한 기피 키워드를 토대로 최악의 일자리를 분석하고 추려내세요.
          </p>
        </div>

        {/* 알약 형태 탭 메뉴 */}
        <div className="store-tabs-wrapper">
          <div className="store-tabs-bar">
            <button 
              className={`tab-btn ${activeTab === "keyword" ? "active" : ""}`}
              onClick={() => setActiveTab("keyword")}
            >
              키워드 ({keywords.length})
            </button>
            <button 
              className={`tab-btn ${activeTab === "analysis" ? "active" : ""}`}
              onClick={() => setActiveTab("analysis")}
            >
              상성 분석
            </button>
            <button 
              className={`tab-btn ${activeTab === "trash" ? "active" : ""}`}
              onClick={() => setActiveTab("trash")}
            >
              휴지통 ({trashItems.length})
            </button>
          </div>
        </div>

        {/* 로딩 인디케이터 */}
        {isLoading && <div className="store-loading-spinner">데이터를 최신화 중입니다...</div>}

        {/* ─── TAB 1: KEYWORD LIST ─── */}
        {!isLoading && activeTab === "keyword" && (
          <div className="store-content-panel anim-fadein">
            {keywords.length > 0 ? (
              <div className="keyword-grid-layout">
                {keywords.map((item) => (
                  <div key={item.tag_id} className="keyword-card-item">
                    <div className="card-top-info">
                      <span className="card-tag-name">🚫 {item.tag_name}</span>
                      <span className="card-tag-weight">누적 {item.accumulated_weight.toFixed(1)}점</span>
                    </div>
                    <p className="card-tag-desc">{item.description || "밸런스 게임을 통해 축적된 기피 항목입니다."}</p>
                    <button className="card-delete-action-btn" onClick={() => handleDeleteKeyword(item.tag_id)}>
                      보관함에서 삭제
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <div className="store-empty-content">
                <p className="empty-msg-text">아직 보관함에 저장된 키워드가 없어요.</p>
                <button className="go-game-btn" onClick={() => window.location.href='/story'}>
                  <span>게임에서 키워드 추출하기 →</span>
                </button>
              </div>
            )}
          </div>
        )}

        {/* ─── TAB 2: AI ANALYSIS REPORT ─── */}
        {!isLoading && activeTab === "analysis" && (
          <div className="store-content-panel anim-fadein">
            {keywords.length === 0 ? (
              <div className="store-empty-content">
                <p className="empty-msg-text">보관함에 등록된 키워드가 있어야 AI 매칭 상성 분석이 가능합니다.</p>
              </div>
            ) : !analysis ? (
              <div className="analysis-trigger-zone">
                <p className="trigger-guide-text">
                  현재 등록된 <strong>{keywords.length}개</strong>의 기피 데이터를 종합 분석하여,<br />
                  당신과 상극인 최악의 직무 환경 리포트를 실시간으로 생성합니다.
                </p>
                <button className="go-game-btn" onClick={handleRunAnalysis} disabled={isAnalyzing}>
                  <span>{isAnalyzing ? "AI 분석 리포트 작성 중..." : "💥 불합치 직업군 실시간 분석"}</span>
                </button>
              </div>
            ) : (
              <div className="analysis-result-report">
                <div className="report-summary-box">
                  <div className="report-badge">종합 진단 요약</div>
                  <h3 className="report-summary-title">"{analysis.summary}"</h3>
                </div>

                <div className="unfit-jobs-container">
                  <h4 className="container-section-title">🚨 당신이 무조건 피해야 할 일자리 Top 2</h4>
                  <div className="unfit-jobs-grid">
                    {analysis.unfit_jobs?.map((job, idx) => (
                      <div key={idx} className="unfit-job-card">
                        <div className="job-card-header">
                          <span className="job-rank-num">0{idx + 1}</span>
                          <h5 className="job-title-text">{job.job_title}</h5>
                        </div>
                        <p className="job-reason-paragraph">{job.reason}</p>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="report-footer-advice">
                  <span>💡 <strong>구직 핵심 가이드:</strong> {analysis.advice}</span>
                </div>
                
                <button className="analysis-retry-action-btn" onClick={handleRunAnalysis} disabled={isAnalyzing}>
                  {isAnalyzing ? "재분석 중..." : "↺ 리포트 다시 추출하기"}
                </button>
              </div>
            )}
          </div>
        )}

        {/* ─── TAB 3: TRASH CAN ─── */}
        {!isLoading && activeTab === "trash" && (
          <div className="store-content-panel anim-fadein">
            {trashItems.length > 0 ? (
              <div className="trash-list-table">
                <div className="trash-table-header">
                  <span>삭제된 키워드명</span>
                  <span>액션</span>
                </div>
                {trashItems.map((item) => (
                  <div key={item.tag_id} className="trash-table-row">
                    <span className="trash-item-title">⏳ {item.tag_name}</span>
                    <button className="trash-restore-action-btn" onClick={() => handleRestoreKeyword(item.tag_id)}>
                      보관함 복구
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <div className="store-empty-content">
                <p className="empty-msg-text">휴지통이 깨끗하게 비어 있습니다.</p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}