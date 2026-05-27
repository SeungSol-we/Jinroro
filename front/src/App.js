import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

import Header from './component/Header';
import MainPage from './pages/MainPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/Signup';
import Story from './pages/Story';
import Store from './pages/Store';
import Setting from './pages/Setting';
import Blacklist from './pages/Blacklist';
import MyPage from './pages/MyPage';

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/main"      element={<MainPage />} />
        <Route path="/login"     element={<LoginPage />} />
        <Route path="/signup"    element={<SignupPage />} />
        <Route path="/story"     element={<Story />} />
        <Route path="/store"     element={<Store />} />
        <Route path="/settings"  element={<Setting />} />
        <Route path="/blacklist" element={<Blacklist />} />
        <Route path="/mypage"    element={<MyPage />} />
        <Route path="/"          element={<Navigate to="/main" />} />
      </Routes>
    </Router>
  );
}

export default App;