import { useMemo, useState } from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { collegeData } from './config/collegeData';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import ProtectedDemoPage from './pages/ProtectedDemoPage';
import ProtectedRoute from './routes/ProtectedRoute';

function App() {
  const [auth, setAuth] = useState(() => {
    const stored = window.sessionStorage.getItem('sdms_phase1_auth');
    return stored ? JSON.parse(stored) : null;
  });

  const setLoginState = (nextState) => {
    setAuth(nextState);
    window.sessionStorage.setItem('sdms_phase1_auth', JSON.stringify(nextState));
  };

  const logout = () => {
    setAuth(null);
    window.sessionStorage.removeItem('sdms_phase1_auth');
  };

  const college = useMemo(() => collegeData, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage college={college} />} />
        <Route path="/login" element={<LoginPage college={college} onLogin={setLoginState} />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />

        <Route element={<ProtectedRoute auth={auth} />}>
          <Route path="/portal" element={<ProtectedDemoPage auth={auth} onLogout={logout} />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
