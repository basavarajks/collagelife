import { useState } from 'react';
import { Link } from 'react-router-dom';
import { authApi, getApiErrorMessage } from '../services/api';

function ProtectedDemoPage({ auth, onLogout }) {
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const checkAccess = async () => {
    setError('');
    setMessage('');
    try {
      const response = await authApi.getProtectedExample(auth.token);
      setMessage(response.data?.data?.message || 'Protected endpoint response received.');
    } catch (requestError) {
      setError(getApiErrorMessage(requestError));
    }
  };

  return (
    <main className="protected-page">
      <section className="auth-card" aria-labelledby="protected-title">
        <h1 id="protected-title">Protected Route Foundation</h1>
        <p>Signed in as: {auth.user?.user_id}</p>
        <p>Role from backend: {auth.user?.role}</p>

        <div className="hero-actions">
          <button type="button" className="button-link button-primary" onClick={checkAccess}>
            Verify protected API
          </button>
          <button type="button" className="button-link button-secondary" onClick={onLogout}>
            Logout
          </button>
        </div>

        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}

        <Link to="/">Return to public homepage</Link>
      </section>
    </main>
  );
}

export default ProtectedDemoPage;
