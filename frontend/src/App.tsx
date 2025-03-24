import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import MarketAnalysis from './pages/MarketAnalysis';
import PropertyComparison from './pages/PropertyComparison';
import '@cloudscape-design/global-styles/index.css';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="market-analysis" element={<MarketAnalysis />} />
          <Route path="property-comparison" element={<PropertyComparison />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App; 