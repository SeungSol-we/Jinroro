import { useState } from "react";
import { useNavigate, useLocation } from 'react-router-dom';
import "./Header.css";

const Header = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [drawerOpen, setDrawerOpen] = useState(false);

  const isActive = (path) => location.pathname === path;

  return (
    <>
      <header className="header">
        {/* 로고 */}
        <button className="header-logo" onClick={() => navigate('/main')}>
          진로<span>로</span>
        </button>

        {/* 오른쪽 버튼들 */}
        <div className="header-right">
          <button className={`header-btn${isActive('/story') ? ' active' : ''}`} onClick={() => navigate('/story')}>
            🎮 싫음 탐색기
          </button>
          <button className={`header-btn${isActive('/store') ? ' active' : ''}`} onClick={() => navigate('/store')}>
            🗑️ 싫음 보관함
          </button>
          <button className={`header-btn${isActive('/blacklist') ? ' active' : ''}`} onClick={() => navigate('/blacklist')}>
            ⚠️ 블랙리스트
          </button>

          {/* 햄버거 메뉴 */}
          <button className="header-menu-btn" onClick={() => setDrawerOpen(true)}>
            <span /><span /><span />
          </button>
        </div>
      </header>

      {/* 헤더 높이 보정 */}
      <div className="header-spacer" />

      {/* 드로어 */}
      {drawerOpen && (
        <>
          <div className="drawer-overlay" onClick={() => setDrawerOpen(false)} />
          <div className="drawer">
            <div className="drawer-header">
              <span className="drawer-title">메뉴</span>
              <button className="drawer-close" onClick={() => setDrawerOpen(false)}>✕</button>
            </div>

            <div className="drawer-menu">
              <button className="drawer-item" onClick={() => { navigate('/login'); setDrawerOpen(false); }}>
                <div>
                  <div className="drawer-item-label">로그인</div>
                </div>
              </button>
            </div>
          </div>
        </>
      )}
    </>
  );
};

export default Header;