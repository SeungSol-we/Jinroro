    import { useState } from "react";
    import { useNavigate, useLocation } from 'react-router-dom';
    import "./Header.css";

    const Header = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const [drawerOpen, setDrawerOpen] = useState(false);

    const isActive = (path) => location.pathname === path;
    const isLoggedIn = !!localStorage.getItem("accessToken");

    const handleLogout = () => {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        setDrawerOpen(false);
        navigate("/login");
    };

    return (
        <>
        <header className="header">
            <button className="header-logo" onClick={() => navigate('/main')}>
            진로로
            </button>

            <div className="header-right">
            <button className={`header-btn${isActive('/story') ? ' active' : ''}`} onClick={() => navigate('/story')}>
                싫음 탐색기
            </button>
            <button className={`header-btn${isActive('/store') ? ' active' : ''}`} onClick={() => navigate('/store')}>
                싫음 보관함
            </button>
            <button className={`header-btn${isActive('/blacklist') ? ' active' : ''}`} onClick={() => navigate('/blacklist')}>
                블랙리스트
            </button>

            <button className="header-menu-btn" onClick={() => setDrawerOpen(true)}>
                <span /><span /><span />
            </button>
            </div>
        </header>

        <div className="header-spacer" />

        {drawerOpen && (
            <>
            <div className="drawer-overlay" onClick={() => setDrawerOpen(false)} />
            <div className="drawer">
                <div className="drawer-header">
                <span className="drawer-title">메뉴</span>
                <button className="drawer-close" onClick={() => setDrawerOpen(false)}>✕</button>
                </div>

                <div className="drawer-menu">
                {isLoggedIn ? (
                    <>
                    <button className="drawer-item" onClick={() => { navigate('/mypage'); setDrawerOpen(false); }}>
                        <div className="drawer-item-label">마이페이지</div>
                    </button>
                    <button className="drawer-item" onClick={() => { navigate('/settings'); setDrawerOpen(false); }}>
                        <div className="drawer-item-label">설정</div>
                    </button>
                    <button className="drawer-item" onClick={handleLogout}>
                        <div className="drawer-item-label">로그아웃</div>
                    </button>
                    </>
                ) : (
                    <button className="drawer-item" onClick={() => { navigate('/login'); setDrawerOpen(false); }}>
                    <div className="drawer-item-label">로그인</div>
                    </button>
                )}
                </div>
            </div>
            </>
        )}
        </>
    );
    };

    export default Header;