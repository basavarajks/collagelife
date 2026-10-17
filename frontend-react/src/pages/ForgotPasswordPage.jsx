import { Link } from 'react-router-dom';

function ForgotPasswordPage() {
  return (
    <main className="auth-page">
      <section className="auth-card" aria-labelledby="forgot-title">
        <h1 id="forgot-title">Forgot Password</h1>
        <p>This feature is not configured yet in Phase 1.</p>
        <p>Please contact authorized administrators once reset workflows are configured.</p>
        <Link to="/login" className="button-link button-primary">
          Back to Login
        </Link>
      </section>
    </main>
  );
}

export default ForgotPasswordPage;
