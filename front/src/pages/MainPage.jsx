import "./MainPage.css";
import { useNavigate } from 'react-router-dom';

const FEATURES = [
  {
    icon: "🎮",
    title: "싫음 탐색기",
    desc: "10개의 선택지를 통해 싫어하는 것들을 찾아내고, 나에게 맞는 직업을 발견하세요.",
    path: "/story",
  },
  {
    icon: "🗑️",
    title: "싫음 보관함",
    desc: "지금까지 발견한 싫은 것들을 정리하고, 분석을 통해 패턴을 찾아보세요.",
    path: "/store",
  },
  {
    icon: "⚠️",
    title: "블랙리스트",
    desc: "피해야 할 회사들의 정보와 선배들의 솔직한 후기를 확인하세요.",
    path: "/blacklist",
  },
  {
    icon: "⚙️",
    title: "설정",
    desc: "당신의 데이터를 관리하고, 언제든지 초기화할 수 있어요.",
    path: "/settings",
  },
];

const MainPage = () => {
  const navigate = useNavigate();

  return (
    <div className="main-root">

      {/* ── 히어로 섹션 ── */}
      <section className="main-hero">
        <div className="main-hero-left">
          <p className="main-hero-tag">✦ 진로 탐색 서비스</p>
          <h1 className="main-hero-slogan">
            싫은 것 부터<br />확실히 알자!
          </h1>
          <p className="main-hero-desc">
            싫어하는 것을 하나씩 골라내면서<br />
            나에게 딱 맞는 진로를 찾아보세요.
          </p>
          <button className="main-hero-btn" onClick={() => navigate('/story')}>
              싫음 탐색기 시작
          </button>
        </div>
        <div className="main-hero-right">
          <div className="main-hero-illust">
            <img src="/main.png" alt="진로 탐색 일러스트" />
          </div>
        </div>
      </section>

      {/* ── 기능 소개 섹션 ── */}
      <section className="main-features">
        <h2 className="main-features-title">어떻게 시작할까요?</h2>
        <div className="main-features-grid">
          {FEATURES.map((f) => (
            <div key={f.title} className="main-feature-card" onClick={() => navigate(f.path)}>
              <div className="main-feature-icon">{f.icon}</div>
              <h3 className="main-feature-title">{f.title}</h3>
              <p className="main-feature-desc">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="main-cta">
        <p className="main-cta-text">지금 바로 시작해서 당신의 진로를 찾아보세요.</p>
        <button className="main-cta-btn" onClick={() => navigate('/story')}>
          시작하기 →
        </button>
      </section>

      {/* ── 푸터 ── */}
      <footer className="main-footer">
        Jinroro - 당신의 진로 탐색 파트너
      </footer>

    </div>
  );
};

export default MainPage;