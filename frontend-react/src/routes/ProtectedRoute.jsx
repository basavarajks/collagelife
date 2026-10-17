import { Navigate, Outlet, useLocation } from 'react-router-dom';

function ProtectedRoute({ auth }) {
  const location = useLocation();

  if (!auth?.token || !auth?.user?.role) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return <Outlet />;
}

export default ProtectedRoute;
