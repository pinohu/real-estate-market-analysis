import axios from 'axios';
import { MarketMetrics } from '../types/market';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

export const getMarketAnalysis = async (location: string, propertyType: string): Promise<MarketMetrics> => {
  try {
    const response = await axios.get<MarketMetrics>(`${API_BASE_URL}/api/market-analysis`, {
      params: { location, propertyType }
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.message || 'Failed to fetch market analysis');
    }
    throw error;
  }
}; 