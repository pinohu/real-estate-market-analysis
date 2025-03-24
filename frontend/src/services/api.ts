import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

export interface PropertyAnalysisRequest {
  address: string;
  city: string;
  state: string;
  zipCode: string;
}

export interface MarketAnalysisRequest {
  city: string;
  state: string;
  radius: number;
}

export interface PropertyAnalysisResponse {
  marketValue: number;
  roiPotential: number;
  marketScore: number;
  demographics: {
    population: number;
    medianIncome: number;
    unemployment: number;
  };
  comparableProperties: Array<{
    address: string;
    price: number;
    squareFeet: number;
    pricePerSqFt: number;
  }>;
}

export interface MarketAnalysisResponse {
  marketHealth: {
    score: number;
    status: string;
  };
  investmentOpportunity: {
    score: number;
    status: string;
  };
  metrics: {
    medianHomePrice: number;
    pricePerSqFt: number;
    daysOnMarket: number;
    inventory: number;
    priceHistory: Array<{
      date: string;
      price: number;
    }>;
  };
}

const api = {
  analyzeProperty: async (data: PropertyAnalysisRequest): Promise<PropertyAnalysisResponse> => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/analyze-property`, data);
      return response.data;
    } catch (error) {
      console.error('Error analyzing property:', error);
      throw error;
    }
  },

  analyzeMarket: async (data: MarketAnalysisRequest): Promise<MarketAnalysisResponse> => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/analyze-market`, data);
      return response.data;
    } catch (error) {
      console.error('Error analyzing market:', error);
      throw error;
    }
  },

  checkHealth: async (): Promise<{ status: string; message: string }> => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/health`);
      return response.data;
    } catch (error) {
      console.error('Error checking API health:', error);
      throw error;
    }
  },
};

export default api; 