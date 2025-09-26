import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Layout } from './components/Layout';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { DashboardPage } from './pages/DashboardPage';
import { IncomePage } from './pages/IncomePage';
import { ExpensesPage } from './pages/ExpensesPage';
import { ProfilePage } from './pages/ProfilePage';
import { AdminPage } from './pages/AdminPage';
import { DemoPage } from './pages/DemoPage';
import { HarvestSeasonsPage } from './pages/HarvestSeasonsPage';
import { EquipmentPage } from './pages/EquipmentPage';
import { HarvestSummaryPage } from './pages/HarvestSummaryPage';
import { useParams } from 'react-router-dom';

// Wrapper components to handle route parameters
const EquipmentPageWrapper = () => {
  const { harvestSeasonId } = useParams<{ harvestSeasonId: string }>();
  return <EquipmentPage harvestSeasonId={parseInt(harvestSeasonId!)} />;
};

const HarvestSummaryPageWrapper = () => {
  const { harvestSeasonId } = useParams<{ harvestSeasonId: string }>();
  return <HarvestSummaryPage harvestSeasonId={parseInt(harvestSeasonId!)} />;
};

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/demo" element={<DemoPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="income" element={<IncomePage />} />
          <Route path="expenses" element={<ExpensesPage />} />
          <Route path="profile" element={<ProfilePage />} />
          <Route path="admin" element={<AdminPage />} />
          <Route path="harvest-seasons" element={<HarvestSeasonsPage />} />
          <Route path="equipment/:harvestSeasonId" element={<EquipmentPageWrapper />} />
          <Route path="summary/:harvestSeasonId" element={<HarvestSummaryPageWrapper />} />
        </Route>
      </Routes>
    </AuthProvider>
  );
}

export default App;
