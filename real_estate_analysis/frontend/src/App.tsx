import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { theme } from './utils/theme';
import Layout from './components/Layout';
import Home from './pages/Home';
import Properties from './pages/Properties';
import Analysis from './pages/Analysis';
import Login from './pages/Login';
import Register from './pages/Register';
import PrivateRoute from './components/PrivateRoute';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route
                path="/properties"
                element={
                  <PrivateRoute>
                    <Properties />
                  </PrivateRoute>
                }
              />
              <Route
                path="/analysis"
                element={
                  <PrivateRoute>
                    <Analysis />
                  </PrivateRoute>
                }
              />
            </Routes>
          </Layout>
        </Router>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App; 