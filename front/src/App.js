import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import './App.css';

import MainPage from './pages/MainPage';
import LoginPage from './pages/LoginPage';
import Story from './pages/Story';  // ← 추가

function App() {
  return (
    <Router>
      <Routes> 
        <Route path="/main" element={<MainPage />} /> 
        <Route path="/login" element={<LoginPage />} /> 
        <Route path="/story" element={<Story />} />  {/* ← 추가 */}

        <Route path="/" element={<Navigate to="/main" />} />
      </Routes> 
    </Router>
  );
}

export default App;