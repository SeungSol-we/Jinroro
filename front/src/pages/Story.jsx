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

  // 고유성 오류를 방지하기 위해 태그의 '명칭(string)'을 기준으로 다중 선택 상태를 관리합니다.
  const [selectedTagNames, setSelectedTagNames] = useState([]);
  const [isSavedToStorage, setIsSavedToStorage] = useState(false);

  const TOTAL_STEPS = 5;

  const fetchNextAiScenario = async () => {
    // 💡 [해결] 다음 질문으로 넘어가기 전, 이전 질문의 흔적(선택 하이라이트)을 확실하게 지웁니다.
    setSelectedLabel(null);
    setIsLoading(true);
    
    try {
      const token = localStorage.getItem("accessToken");
      if (!token) {
        alert("로그인이 필요합니다.");
        navigate("/");
        return;
      }

      const response = await fetch("http://localhost:8000/balance/ai/scenario", {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });

      if (!response.ok) {
        if (response.status === 400) {
          alert("백엔드에 seed 데이터가 없습니다. seed를 먼저 실행해 주세요!");
        }
        throw new Error("AI 시나리오를 가져오는 데 실패했습니다.");
      }

      const data = await response.json();
      console.log("AI가 생성한 시나리오:", data);
      setCurrentScenario(data);
    } catch (error) {
      console.error(error);
      alert("다음 시나리오를 불러오는 중 오류가 발생했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  const startGame = async () => {
    setStep(1);
    setPhase("game");
    await fetchNextAiScenario();
  };

  const handleSelect = async (choice) => {
    if (selectedLabel !== null || isLoading) return;
    setSelectedLabel(choice.label);

    const token = localStorage.getItem("accessToken");
    if (!token) {
      alert("로그인이 필요합니다. 로그인 화면으로 이동합니다.");
      navigate("/");
      return;
    }

    setIsLoading(true);

    const rawScenarioId = currentScenario.ai_scenario_id !== undefined ? currentScenario.ai_scenario_id : currentScenario.id;

    const requestBody = {
      ai_scenario_id: Number(rawScenarioId),
      selected_label: String(choice.label),
      selected_fear_tag_id: choice.fear_tag_id ? Number(choice.fear_tag_id) : null
    };

    console.log("프론트가 백엔드로 보낼 전송 데이터:", requestBody);

    try {
      const response = await fetch("http://localhost:8000/balance/ai/answers", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(requestBody),
      });

      if (response.status === 401) {
        localStorage.removeItem("accessToken");
        alert("로그인 세션이 만료되었습니다. 다시 로그인 해주세요.");
        navigate("/");
        return;
      }

      if (!response.ok) {
        const errorDetail = await response.json().catch(() => ({}));
        console.error("백엔드가 뱉은 실제 에러 내용:", errorDetail);
        throw new Error("답변 제출 실패");
      }

      // 선택 모션 유지를 위한 타이머 실행 후 스텝 전환
      setTimeout(async () => {
        if (step >= TOTAL_STEPS) {
          await fetchFinalResults(token);
          setPhase("result");
        } else {
          setStep((prev) => prev + 1);
          await fetchNextAiScenario();
        }
      }, 450);

    } catch (error) {
      console.error(error);
      alert("답변을 처리하는 중 오류가 발생했습니다. (콘솔창의 백엔드 에러 내용을 확인하세요)");
      setSelectedLabel(null);
      setIsLoading(false);
    }
  };

  const fetchFinalResults = async (token) => {
    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:8000/balance/avoid-tags", {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (!response.ok) throw new Error("최종 결과 조회 실패");
      const tagsData = await response.json();
      setAvoidTags(tagsData);
    } catch (error) {
      console.error("결과 파싱 오류:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // 결과창 리스트 클릭 시 개별 토글 처리
  const handleToggleTag = (tagName) => {
    if (isSavedToStorage) return; 
    if (selectedTagNames.includes(tagName)) {
      setSelectedTagNames(selectedTagNames.filter(name => name !== tagName));
    } else {
      setSelectedTagNames([...selectedTagNames, tagName]);
    }
  };

  // 💡 [해결] 백엔드 라우터 구조(단건 순회 처리)에 최적화하여 전송하는 함수
  const saveToDislikeStorage = async () => {
    if (selectedTagNames.length === 0) {
      alert("보관함에 넣을 키워드를 하나 이상 선택해 주세요!");
      return;
    }

    const token = localStorage.getItem("accessToken");
    setIsLoading(true);

    // 1. 선택된 태그명들을 기반으로 백엔드용 tag_id 목록을 정제 추출합니다.
    const finalTargetIds = avoidTags
      .filter(tag => selectedTagNames.includes(tag.tag_name))
      .map(tag => tag.fear_tag_id || tag.id)
      .filter(id => id !== undefined && id !== null);

    try {
      // 2. 백엔드 라우터 규칙인 `POST /balance/avoid-tags/manual` 주소로 
      //    선택한 키워드 개수만큼 비동기 요청을 동시에 전부 쏩니다.
      const requestPromises = finalTargetIds.map(tagId =>
        fetch("http://localhost:8000/balance/avoid-tags/manual", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify({ tag_id: tagId }), // ManualTagRequest 포맷 통일
        })
      );

      // 모든 API 요청이 끝날 때까지 대기합니다.
      const responses = await Promise.all(requestPromises);

      // 하나라도 실패한 요청이 있는지 검증합니다.
      const anyFailed = responses.some(res => !res.ok);
      if (anyFailed) {
        throw new Error("일부 키워드를 보관함에 넣지 못했습니다.");
      }

      alert("🔒 선택하신 키워드가 '싫음 보관함'에 안전하게 보관되었습니다!");
      setIsSavedToStorage(true);
    } catch (error) {
      console.error(error);
      alert("보관함 저장 중 에러가 발생했습니다. 백엔드 매핑 데이터를 다시 체크하세요.");
    } finally {
      setIsLoading(false);
    }
  };

  const restart = () => {
    setPhase("intro");
    setStep(0);
    setCurrentScenario(null);
    setSelectedLabel(null);
    setAvoidTags([]);
    setSelectedTagNames([]);       
    setIsSavedToStorage(false);   
  };

  const progress = (step / TOTAL_STEPS) * 100;

  return (
    <div className="story-root">
      {/* ─── INTRO PHASE ─── */}
      {phase === "intro" && (
        <div className="intro-container anim-fadeup">
          <div className="intro-wrap">
            <div className="intro-badge">✨ GPT AI 실시간 연동 테스트</div>
            <h1 className="intro-title">
              AI가 설계하는<br />
              <span className="accent-color">나의 커리어 피해야 할 조건</span>
            </h1>
            <p className="intro-desc">
              AI가 당신의 성향을 자극하는 스토리를 실시간으로 만듭니다.
            </p>
            <button className="start-btn" onClick={startGame} disabled={isLoading}>
              <span>{isLoading ? "AI 시나리오 준비 중..." : "테스트 시작하기"}</span>
              <span>→</span>
            </button>
          </div>
        </div>
      )}

      {/* ─── GAME PHASE ─── */}
      {phase === "game" && currentScenario && (
        <div className="game-container anim-fadeIn">
          <div className="game-top-bar">
            <div className="game-status">
              <span className="game-step">질문 {step} / {TOTAL_STEPS}</span>
              <button onClick={restart} className="game-restart-link">✕ 처음으로</button>
            </div>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${progress}%` }} />
            </div>
          </div>

          <div className="game-content-wrap">
            <h2 className="game-question-text">
              {currentScenario.scenario_title}
            </h2>

            <div className="game-story-box">
              <p className="game-story-paragraph">{currentScenario.scenario_description}</p>
            </div>

            <div className="game-options-list">
              {currentScenario.choices?.map((choice, idx) => (
                <button
                  key={idx}
                  className={`story-btn${selectedLabel === choice.label ? " selected" : ""}`}
                  onClick={() => handleSelect(choice)}
                  disabled={isLoading}
                  style={{ opacity: selectedLabel && selectedLabel !== choice.label ? 0.45 : 1 }}
                >
                  <div className="label-badge">
                    {choice.label === "left" ? "A" : "B"}
                  </div>
                  <div className="option-text-wrap">
                    <div className="option-main-text">{choice.text}</div>
                    <div style={{ fontSize: "11px", color: "#ef4444", marginTop: "4px", opacity: 0.6 }}>
                      (기피 자극 요인: {choice.keyword})
                    </div>
                  </div>
                  {selectedLabel === choice.label && <div className="option-check-badge">✓</div>}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ─── RESULT PHASE ─── */}
      {phase === "result" && (
        <div className="result-container anim-pop">
          <div className="result-wrap">
            <div className="result-header">
              <div className="result-emoji-anim">🚫</div>
              <br />
              <div className="result-badge" style={{ background: "#fee2e2", color: "#ef4444" }}>
                AI 커리어 기피 종합 진단 결과
              </div>
              <h1 className="result-type-title">당신이 가장 멀리해야 할 일자리 환경</h1>
              <p style={{ fontSize: "14px", color: "#6b7280", marginTop: "8px" }}>
                보관함에 넣고 관리할 기피 키워드를 선택해 주세요.
              </p>
            </div>

            <div className="result-jobs-box">
              <div className="result-jobs-title">누적된 나의 기피 태그 순위 (클릭하여 개별 선택 가능)</div>
              <div className="result-jobs-list" style={{ gap: "12px", flexDirection: "column" }}>
                {avoidTags.length > 0 ? (
                  avoidTags.map((tag, idx) => {
                    const isChecked = selectedTagNames.includes(tag.tag_name);

                    return (
                      <div
                        key={idx}
                        onClick={() => handleToggleTag(tag.tag_name)}
                        style={{
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "space-between",
                          width: "100%",
                          padding: "14px 20px",
                          background: isChecked ? "#f5f3ff" : "#fafaf9",
                          border: isChecked ? "2px solid #7c3aed" : "1.5px solid #e7e5e4",
                          color: isChecked ? "#7c3aed" : "#44403c",
                          fontWeight: isChecked || idx === 0 ? "700" : "500",
                          borderRadius: "12px",
                          cursor: isSavedToStorage ? "not-allowed" : "pointer",
                          transition: "all 0.2s ease",
                          boxShadow: isChecked ? "0 4px 12px rgba(124,58,237,0.08)" : "none"
                        }}
                      >
                        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                          <input 
                            type="checkbox" 
                            checked={isChecked}
                            disabled={isSavedToStorage}
                            onChange={() => {}} 
                            style={{ 
                              width: "18px", 
                              height: "18px", 
                              accentColor: "#7c3aed",
                              cursor: isSavedToStorage ? "not-allowed" : "pointer" 
                            }}
                          />
                          <span>{idx + 1}. {tag.tag_name}</span>
                        </div>
                        <span style={{ fontSize: "13px", opacity: 0.7 }}>
                          누적 기피도: {tag.accumulated_weight ? tag.accumulated_weight.toFixed(1) : 0}점
                        </span>
                      </div>
                    );
                  })
                ) : (
                  <p style={{ color: "#a8a29e", textAlign: "center" }}>선택 데이터가 부족하여 분석된 키워드가 없습니다.</p>
                )}
              </div>
            </div>

            {/* 싫음 보관함 액션 영역 */}
            <div className="result-actions" style={{ display: "flex", flexDirection: "column", gap: "12px", marginTop: "24px" }}>
              <button 
                className="start-btn"
                onClick={saveToDislikeStorage}
                disabled={isLoading || isSavedToStorage || selectedTagNames.length === 0}
                style={{
                  width: "100%",
                  justifyContent: "center",
                  borderRadius: "14px",
                  padding: "18px",
                  background: isSavedToStorage ? "#10b981" : selectedTagNames.length === 0 ? "#cbd5e1" : "#7c3aed",
                  color: "#fff",
                  cursor: (isLoading || isSavedToStorage || selectedTagNames.length === 0) ? "not-allowed" : "pointer",
                }}
              >
                {isSavedToStorage ? "✓ 보관함 저장 완료" : `📥 선택한 ${selectedTagNames.length}개 키워드 싫음 보관함에 넣기`}
              </button>

              <button className="restart-btn" onClick={restart} style={{ width: "100%", justifyContent: "center", borderRadius: "14px", padding: "14px" }}>
                <span>새로운 AI 시나리오로 다시 풀기</span>
                <span>↺</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}