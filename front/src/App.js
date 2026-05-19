import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import './App.css';

// 페이지 컴포넌트 불러오기
import MainPage from './pages/MainPage';
import LoginPage from './pages/LoginPage';

function App() {
  return (
    <Router>
      <Routes> 
        <Route path="/main" element={<MainPage />} /> 
        <Route path="/login" element={<LoginPage />} /> 

        <Route path="/" element={<Navigate to="/main" />} />
      </Routes> 
    </Router>
  );
}

export default App;
