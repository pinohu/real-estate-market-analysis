import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import '@cloudscape-design/global-styles/index.css';

import Dashboard from './pages/Dashboard';
import PropertyAnalysis from './pages/PropertyAnalysis';
import MarketAnalysis from './pages/MarketAnalysis';
import Settings from './pages/Settings';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/property-analysis" element={<PropertyAnalysis />} />
        <Route path="/market-analysis" element={<MarketAnalysis />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Router>
  );
};

export default App; 