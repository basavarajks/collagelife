import { Eye, EyeOff, Loader2, LogIn } from 'lucide-react';
import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import ImageWithFallback from '../components/ImageWithFallback';
import { supportedRoles } from '../config/collegeData';
import { authApi, getApiErrorMessage } from '../services/api';

function LoginPage({ college, onLogin }) {
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ user_id: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const from = location.state?.from?.pathname || '/portal';

  const submit = async (event) => {
    event.preventDefault(); setError('');
    if (!form.user_id.trim() || !form.password) { setError('User ID and password are required.'); return; }
    try {
      setLoading(true);
      const response = await authApi.login({ user_id: form.user_id.trim(), password: form.password });
      const { token, user } = response.data?.data || {};
      if (!token || !user?.role) throw new Error('Invalid authentication response from server.');
      onLogin({ token, user }); navigate(from, { replace: true });
    } catch (requestError) { setError(requestError.message?.startsWith('Invalid authentication') ? requestError.message : getApiErrorMessage(requestError)); }
    finally { setLoading(false); }
  };

  return <main className="auth-page"><section className="auth-card" aria-labelledby="login-title">
    <ImageWithFallback src={college.logo} alt={`${college.name} logo`} className="auth-logo" fallbackText="Logo unavailable" />
    <h1 id="login-title">SDMS Login Portal</h1><p>{college.name}</p>
    <form onSubmit={submit} noValidate>
      <label htmlFor="user_id">User ID</label>
      <input id="user_id" name="user_id" type="text" autoComplete="username" value={form.user_id} onChange={(e) => setForm((p) => ({ ...p, user_id: e.target.value }))} required />
      <label htmlFor="password">Password</label>
      <div className="password-row"><input id="password" name="password" type={showPassword ? 'text' : 'password'} autoComplete="current-password" value={form.password} onChange={(e) => setForm((p) => ({ ...p, password: e.target.value }))} required /><button type="button" className="icon-button" aria-label={showPassword ? 'Hide password' : 'Show password'} onClick={() => setShowPassword((v) => !v)}>{showPassword ? <EyeOff size={16} /> : <Eye size={16} />}</button></div>
      {error && <p className="error-message" role="alert">{error}</p>}
      <button type="submit" className="button-link button-primary full-width" disabled={loading}>{loading ? <Loader2 className="spin" size={16} /> : <LogIn size={16} />}<span>{loading ? 'Signing in…' : 'Login'}</span></button>
    </form>
    <div className="auth-links"><Link to="/forgot-password">Forgot Password?</Link><Link to="/">Return to Home</Link></div>
    <section className="role-note" aria-label="Role support information"><h2>Supported roles</h2><ul>{supportedRoles.map((role) => <li key={role}>{role}</li>)}</ul><p>Role and permissions are loaded from the authenticated backend session.</p></section>
  </section></main>;
}
export default LoginPage;
