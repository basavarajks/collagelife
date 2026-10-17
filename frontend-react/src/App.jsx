import { useEffect, useMemo, useState } from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { collegeData } from './config/collegeData';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import ProtectedDemoPage from './pages/ProtectedDemoPage';
import AdminDashboard from './pages/AdminDashboard';
import HODDashboard from './pages/HODDashboard';
import ProtectedRoute from './routes/ProtectedRoute';
import { authApi } from './services/api';
import './styles/admin.css';
import './styles/hod.css';

function App() {
  const [auth, setAuth] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);
  const college = useMemo(() => collegeData, []);
  useEffect(() => { const token = window.sessionStorage.getItem('sdms_auth_token'); if (!token) { setAuthLoading(false); return; } authApi.me().then((r) => setAuth({ token, user: r.data?.data?.user })).catch(() => window.sessionStorage.removeItem('sdms_auth_token')).finally(() => setAuthLoading(false)); }, []);
  const setLoginState = (nextState) => { window.sessionStorage.setItem('sdms_auth_token', nextState.token); setAuth(nextState); };
  const logout = async () => { try { await authApi.logout(); } catch {} window.sessionStorage.removeItem('sdms_auth_token'); setAuth(null); };
  if (authLoading) return <main className="auth-page"><section className="auth-card"><p>Checking authentication…</p></section></main>;
  const isAdmin = auth?.user?.role === 'ADMIN_PRINCIPAL';
  const isHod = auth?.user?.role === 'HOD';
  return <BrowserRouter><Routes><Route path="/" element={<HomePage college={college} />} /><Route path="/login" element={<LoginPage college={college} onLogin={setLoginState} />} /><Route path="/forgot-password" element={<ForgotPasswordPage />} /><Route element={<ProtectedRoute auth={auth} />}><Route path="/portal" element={isAdmin ? <AdminDashboard auth={auth} onLogout={logout} /> : isHod ? <HODDashboard auth={auth} onLogout={logout} /> : <ProtectedDemoPage auth={auth} onLogout={logout} />} /></Route><Route path="*" element={<Navigate to="/" replace />} /></Routes></BrowserRouter>;
}
export default App;
