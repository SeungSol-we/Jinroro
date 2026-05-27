import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Story.css";

export default function Story() {
  const navigate = useNavigate();

  const [phase, setPhase] = useState("intro");
  const [currentScenario, setCurrentScenario] = useState(null);
  const [step, setStep] = useState(0);
  const [selectedLabel, setSelectedLabel] = useState(null);
  const [avoidTags, setAvoidTags] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // 💡 실시간 저장 대신 점수를 쌓을 로컬 변수
  const [tempScores, setTempScores] = useState({});
  const [selectedTagNames, setSelectedTagNames] = useState([]);
  const [isSavedToStorage, setIsSavedToStorage] = useState(false);

  const TOTAL_STEPS = 5;

  const fetchNextAiScenario = async () => {
    setSelectedLabel(null);
    setIsLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      const response = await fetch("http://localhost:8000/balance/ai/scenario", {
        headers: { "Authorization": `Bearer ${token}` }
      });
      const data = await response.json();
      setCurrentScenario(data);
    } catch (e) { console.error(e); } finally { setIsLoading(false); }
  };

  const startGame = async () => {
    setStep(1); setPhase("game"); setTempScores({}); 
    await fetchNextAiScenario();
  };

  const handleSelect = async (choice) => {
    if (selectedLabel !== null || isLoading) return;
    setSelectedLabel(choice.label);
    const token = localStorage.getItem("accessToken");
    setIsLoading(true);

    // 💡 1. 프론트엔드 점수 누적 (매우 중요: tag_id를 정확히 저장)
    const tid = choice.fear_tag_id;
    const tname = choice.keyword;
    
    // 비동기 문제를 피하기 위해 최신 값을 직접 계산
    const updatedScores = {
      ...tempScores,
      [tid]: {
        tag_id: tid,
        tag_name: tname,
        accumulated_weight: (tempScores[tid]?.accumulated_weight || 0) + 1.2
      }
    };
    setTempScores(updatedScores);

    try {
      const rid = currentScenario.ai_scenario_id || currentScenario.id;
      await fetch("http://localhost:8000/balance/ai/answers", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
        body: JSON.stringify({
          ai_scenario_id: Number(rid),
          selected_label: String(choice.label),
          selected_fear_tag_id: Number(tid)
        }),
      });

      setTimeout(async () => {
        if (step >= TOTAL_STEPS) {
          // 💡 2. 게임 종료 시 누적된 점수를 결과창 리스트로 변환
          const sorted = Object.values(updatedScores).sort((a, b) => b.accumulated_weight - a.accumulated_weight);
          setAvoidTags(sorted);
          setPhase("result");
        } else {
          setStep((prev) => prev + 1);
          await fetchNextAiScenario();
        }
      }, 450);
    } catch (e) { console.error(e); setIsLoading(false); }
  };

  const handleToggleTag = (tagName) => {
    if (isSavedToStorage) return; 
    setSelectedTagNames(prev => prev.includes(tagName) ? prev.filter(n => n !== tagName) : [...prev, tagName]);
  };

  // 💡 [핵심] 저장 함수
  const saveToDislikeStorage = async () => {
    if (selectedTagNames.length === 0) { alert("항목을 선택해주세요."); return; }
    const token = localStorage.getItem("accessToken");
    setIsLoading(true);

    // 💡 avoidTags 배열에서 선택된 이름과 일치하는 tag_id만 추출
    const targetIds = avoidTags
      .filter(t => selectedTagNames.includes(t.tag_name))
      .map(t => t.tag_id);

    try {
      // 💡 한 개씩 백엔드로 전송 (백엔드 구조에 맞춤)
      for (const tagId of targetIds) {
        const res = await fetch("http://localhost:8000/balance/avoid-tags/manual", {
          method: "POST",
          headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
          body: JSON.stringify({ tag_id: Number(tagId) }),
        });
        if (!res.ok) throw new Error("저장 실패");
      }

      alert("🔒 선택한 키워드가 보관함에 저장되었습니다!");
      setIsSavedToStorage(true);
    } catch (e) { 
      console.error(e);
      alert("보관함 저장 중 오류가 발생했습니다."); 
    } finally { setIsLoading(false); }
  };

  const restart = () => {
    setPhase("intro"); setStep(0); setCurrentScenario(null);
    setSelectedLabel(null); setAvoidTags([]); setSelectedTagNames([]); setIsSavedToStorage(false);
  };

  return (
    <div className="story-root">
      {/* ─── INTRO ─── */}
      {phase === "intro" && (
        <div className="intro-container anim-fadeup">
          <div className="intro-wrap">
            <div className="intro-badge">✨ GPT AI 실시간 연동 테스트</div>
            <h1 className="intro-title">AI가 설계하는<br /><span className="accent-color">나의 커리어 피해야 할 조건</span></h1>
            <p className="intro-desc">AI가 당신의 성향을 자극하는 스토리를 실시간으로 만듭니다.</p>
            <button className="start-btn" onClick={startGame}><span>테스트 시작하기</span><span>→</span></button>
          </div>
        </div>
      )}

      {/* ─── GAME ─── */}
      {phase === "game" && currentScenario && (
        <div className="game-container anim-fadeIn">
          <div className="game-top-bar">
            <div className="game-status">
              <span className="game-step">질문 {step} / {TOTAL_STEPS}</span>
              <button onClick={restart} className="game-restart-link">✕ 처음으로</button>
            </div>
            <div className="progress-bar"><div className="progress-fill" style={{ width: `${(step/TOTAL_STEPS)*100}%` }} /></div>
          </div>
          <div className="game-content-wrap">
            <h2 className="game-question-text">{currentScenario.scenario_title}</h2>
            <div className="game-story-box"><p className="game-story-paragraph">{currentScenario.scenario_description}</p></div>
            <div className="game-options-list">
              {currentScenario.choices?.map((choice, idx) => (
                <button key={idx} className={`story-btn${selectedLabel === choice.label ? " selected" : ""}`} onClick={() => handleSelect(choice)}>
                  <div className="label-badge">{choice.label === "left" ? "A" : "B"}</div>
                  <div className="option-text-wrap">
                    <div className="option-main-text">{choice.text}</div>
                    <div style={{ fontSize: "11px", color: "#ef4444", marginTop: "4px", opacity: 0.6 }}>(기피 자극 요인: {choice.keyword})</div>
                  </div>
                  {selectedLabel === choice.label && <div className="option-check-badge">✓</div>}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ─── RESULT ─── */}
      {phase === "result" && (
        <div className="result-container anim-pop">
          <div className="result-wrap">
            <div className="result-header">
              <div className="result-emoji-anim">🚫</div><br />
              <div className="result-badge" style={{ background: "#fee2e2", color: "#ef4444" }}>AI 커리어 기피 종합 진단 결과</div>
              <h1 className="result-type-title">당신이 가장 멀리해야 할 일자리 환경</h1>
              <p style={{ fontSize: "14px", color: "#6b7280", marginTop: "8px" }}>보관함에 넣고 관리할 기피 키워드를 선택해 주세요.</p>
            </div>
            <div className="result-jobs-box">
              <div className="result-jobs-title">누적된 나의 기피 태그 순위</div>
              <div className="result-jobs-list" style={{ gap: "12px", flexDirection: "column", display: "flex" }}>
                {avoidTags.map((tag, idx) => {
                  const isChecked = selectedTagNames.includes(tag.tag_name);
                  return (
                    <div key={idx} onClick={() => handleToggleTag(tag.tag_name)} style={{
                      display: "flex", alignItems: "center", justifyContent: "space-between", width: "100%", padding: "14px 20px",
                      background: isChecked ? "#f5f3ff" : "#fafaf9", border: isChecked ? "2px solid #7c3aed" : "1.5px solid #e7e5e4",
                      color: isChecked ? "#7c3aed" : "#44403c", borderRadius: "12px", cursor: isSavedToStorage ? "not-allowed" : "pointer", transition: "all 0.2s ease"
                    }}>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                        <input type="checkbox" checked={isChecked} readOnly style={{ width: "18px", height: "18px", accentColor: "#7c3aed" }} />
                        <span>{idx + 1}. {tag.tag_name}</span>
                      </div>
                      <span style={{ fontSize: "13px", opacity: 0.7 }}>누적 기피도: {tag.accumulated_weight.toFixed(1)}점</span>
                    </div>
                  );
                })}
              </div>
            </div>
            <div className="result-actions" style={{ display: "flex", flexDirection: "column", gap: "12px", marginTop: "24px" }}>
              <button className="start-btn" onClick={saveToDislikeStorage} disabled={isSavedToStorage || selectedTagNames.length === 0} style={{ width: "100%", background: isSavedToStorage ? "#10b981" : selectedTagNames.length === 0 ? "#cbd5e1" : "#7c3aed", color: "#fff" }}>
                {isSavedToStorage ? "✓ 보관함 저장 완료" : `📥 선택한 ${selectedTagNames.length}개 키워드 보관함에 넣기`}
              </button>
              <button className="restart-btn" onClick={restart} style={{ width: "100%" }}>새로운 시나리오로 다시 풀기 ↺</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}