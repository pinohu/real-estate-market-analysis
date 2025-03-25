export interface PriceHistoryPoint {
  date: string;
  value: number;
}

export interface MarketMetrics {
  medianPrice: number;
  priceHistory: PriceHistoryPoint[];
  daysOnMarket: number;
  inventoryLevel: string;
  pricePerSqFt: number;
  yearOverYearChange: number;
} 