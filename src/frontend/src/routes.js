import React from 'react';
import { Navigate } from 'react-router-dom';
import DashboardLayout from './layouts/DashboardLayout';
import MainLayout from './layouts/MainLayout';
import DashboardView from './views/reports/DashboardView';
import LoginView from './views/auth/LoginView';
import NotFoundView from './views/errors/NotFoundView';
import PatientListView from './views/patient/PatientListView';
import PickupListView from './views/pickup/PickupListView';
import PickupView from './views/pickup/PickupView';
import isLoggedIn from './utils/isLoggedIn';

const routes = () => {
  let loginStatus = false;
  loginStatus = isLoggedIn();
  return [
    {
      path: 'app',
      element: loginStatus ? <DashboardLayout /> : <LoginView />,
      children: [
        { path: 'pickups', element: <PickupListView /> },
        { path: 'pickup/:id', element: <PickupView />},
        { path: '*', element: <Navigate to="/404" /> }
      ]
    },
    {
      path: '/',
      element: loginStatus ? <DashboardLayout /> : <LoginView />,
      children: [
        { path: 'login', element: <LoginView /> },
        { path: '404', element: <NotFoundView /> },
        { path: '*', element: <Navigate to="/404" /> }
      ]
    }
  ];
};

export default routes;
