import React from 'react';
import { Navigate } from 'react-router-dom';
import DashboardLayout from './layouts/DashboardLayout';
import MainLayout from './layouts/MainLayout';
import DashboardView from './views/reports/DashboardView';
import LoginView from './views/auth/LoginView';
import NotFoundView from './views/errors/NotFoundView';
import PatientListView from './views/patient/PatientListView';
import PickupListView from './views/pickup/PickupListView';


const routes = () => {
  const loginVal = JSON.parse(localStorage.getItem("login"));
  let isLoggedIn = false;
  if (loginVal !== null) {
    isLoggedIn = loginVal.login ?? false;
  }
  return [
    {
      path: 'app',
      element: isLoggedIn ? <DashboardLayout /> : <LoginView />,
      children: [
        { path: 'patients', element: <PatientListView /> },
        { path: 'dashboard', element: <DashboardView /> },
        { path: 'pickups', element: <PickupListView /> },
        { path: '*', element: <Navigate to="/404" /> }
      ]
    },
    {
      path: '/',
      element: isLoggedIn ? <MainLayout /> : <LoginView />,
      children: [
        { path: 'login', element: <LoginView /> },
        { path: '404', element: <NotFoundView /> },
        { path: '/', element: <Navigate to="/app/dashboard" /> },
        { path: '*', element: <Navigate to="/404" /> }
      ]
    }
  ];
};

export default routes;
