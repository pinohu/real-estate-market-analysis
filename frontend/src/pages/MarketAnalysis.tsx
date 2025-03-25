import React, { useState } from 'react';
import {
  Container,
  Header,
  SpaceBetween,
  Button,
  Form,
  FormField,
  Input,
  LineChart,
  Box,
  Alert,
  ColumnLayout
} from '@cloudscape-design/components';
import { MarketMetrics, PriceHistoryPoint } from '../types/market';
import { getMarketAnalysis } from '../services/marketService';

const MarketAnalysis: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [location, setLocation] = useState('');
  const [propertyType, setPropertyType] = useState('');
  const [analysisResults, setAnalysisResults] = useState<MarketMetrics | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!location || !propertyType) {
      setError('Please fill in all required fields');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const data = await getMarketAnalysis(location, propertyType);
      setAnalysisResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch market analysis. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container>
      <SpaceBetween size="l">
        <Header
          variant="h1"
          description="Analyze market trends and conditions for specific locations"
        >
          Market Analysis
        </Header>

        {error && (
          <Alert type="error" dismissible onDismiss={() => setError(null)}>
            {error}
          </Alert>
        )}

        <Form
          actions={
            <Button
              variant="primary"
              onClick={handleAnalyze}
              loading={isLoading}
            >
              Analyze Market
            </Button>
          }
        >
          <SpaceBetween size="l">
            <ColumnLayout columns={2}>
              <FormField label="Location" constraintText="Required">
                <Input
                  value={location}
                  onChange={e => setLocation(e.detail.value)}
                  placeholder="Enter city, state or ZIP code"
                />
              </FormField>
              <FormField label="Property Type" constraintText="Required">
                <Input
                  value={propertyType}
                  onChange={e => setPropertyType(e.detail.value)}
                  placeholder="e.g., Single Family, Condo"
                />
              </FormField>
            </ColumnLayout>
          </SpaceBetween>
        </Form>

        {analysisResults && (
          <SpaceBetween size="l">
            <Box variant="h2">Market Analysis Results</Box>
            <ColumnLayout columns={2}>
              <Box>
                <SpaceBetween size="m">
                  <div>
                    <Box variant="awsui-key-label">Median Price</Box>
                    <Box variant="h3">${analysisResults.medianPrice.toLocaleString()}</Box>
                  </div>
                  <div>
                    <Box variant="awsui-key-label">Days on Market</Box>
                    <Box variant="h3">{analysisResults.daysOnMarket} days</Box>
                  </div>
                  <div>
                    <Box variant="awsui-key-label">Price per Sq Ft</Box>
                    <Box variant="h3">${analysisResults.pricePerSqFt}</Box>
                  </div>
                </SpaceBetween>
              </Box>
              <Box>
                <SpaceBetween size="m">
                  <div>
                    <Box variant="awsui-key-label">Inventory Level</Box>
                    <Box variant="h3">{analysisResults.inventoryLevel}</Box>
                  </div>
                  <div>
                    <Box variant="awsui-key-label">Year over Year Change</Box>
                    <Box variant="h3">{analysisResults.yearOverYearChange}%</Box>
                  </div>
                </SpaceBetween>
              </Box>
            </ColumnLayout>

            <Box>
              <Header variant="h3">Price Trends</Header>
              <LineChart
                series={[
                  {
                    title: 'Median Price',
                    type: 'line',
                    data: analysisResults.priceHistory.map((point: PriceHistoryPoint) => ({
                      x: new Date(point.date),
                      y: point.value
                    }))
                  }
                ]}
                xDomain={[
                  new Date(analysisResults.priceHistory[0].date),
                  new Date(analysisResults.priceHistory[analysisResults.priceHistory.length - 1].date)
                ]}
                yDomain={[
                  Math.min(...analysisResults.priceHistory.map((p: PriceHistoryPoint) => p.value)) * 0.9,
                  Math.max(...analysisResults.priceHistory.map((p: PriceHistoryPoint) => p.value)) * 1.1
                ]}
                i18nStrings={{
                  xTickFormatter: (date: Date) => date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' })
                }}
              />
            </Box>
          </SpaceBetween>
        )}
      </SpaceBetween>
    </Container>
  );
};

export default MarketAnalysis; 