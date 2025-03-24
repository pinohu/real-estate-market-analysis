import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Header,
  LineChart,
  Link,
  Spinner,
  Table
} from '@cloudscape-design/components';
import Layout from '../components/Layout';

interface MarketMetric {
  name: string;
  value: string;
  change: string;
  trend: 'positive' | 'negative' | 'neutral';
}

const Dashboard: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [marketMetrics, setMarketMetrics] = useState<MarketMetric[]>([]);
  const [priceData, setPriceData] = useState<any[]>([]);

  useEffect(() => {
    // Simulated data loading
    setTimeout(() => {
      setMarketMetrics([
        {
          name: 'Median Home Price',
          value: '$425,000',
          change: '+5.2%',
          trend: 'positive'
        },
        {
          name: 'Average Days on Market',
          value: '45',
          change: '-3',
          trend: 'positive'
        },
        {
          name: 'Inventory',
          value: '12,450',
          change: '-2.1%',
          trend: 'negative'
        },
        {
          name: 'Interest Rate',
          value: '6.8%',
          change: '+0.2%',
          trend: 'negative'
        }
      ]);

      setPriceData([
        { x: new Date('2023-01'), y: 400000 },
        { x: new Date('2023-02'), y: 405000 },
        { x: new Date('2023-03'), y: 410000 },
        { x: new Date('2023-04'), y: 415000 },
        { x: new Date('2023-05'), y: 420000 },
        { x: new Date('2023-06'), y: 425000 }
      ]);

      setIsLoading(false);
    }, 1500);
  }, []);

  return (
    <Layout activeHref="/" isLoading={isLoading}>
      <Container>
        <Grid
          gridDefinition={[
            { colspan: { default: 12, xxs: 12 } },
            { colspan: { default: 12, xxs: 12 } }
          ]}
        >
          <Box margin={{ bottom: 'l' }}>
            <Table
              columnDefinitions={[
                {
                  id: 'name',
                  header: 'Metric',
                  cell: item => item.name
                },
                {
                  id: 'value',
                  header: 'Value',
                  cell: item => item.value
                },
                {
                  id: 'change',
                  header: 'Change',
                  cell: item => (
                    <Box color={item.trend === 'positive' ? 'text-status-success' : 'text-status-error'}>
                      {item.change}
                    </Box>
                  )
                }
              ]}
              items={marketMetrics}
              loading={isLoading}
              loadingText="Loading market metrics"
              header={
                <Header
                  variant="h2"
                  description="Key market indicators and their recent changes"
                >
                  Market Metrics
                </Header>
              }
            />
          </Box>

          <Box>
            <Header
              variant="h2"
              description="6-month price trend in the market"
            >
              Price Trends
            </Header>
            {isLoading ? (
              <Spinner />
            ) : (
              <LineChart
                series={[
                  {
                    title: 'Median Home Price',
                    type: 'line',
                    data: priceData
                  }
                ]}
                xDomain={[priceData[0]?.x, priceData[priceData.length - 1]?.x]}
                yDomain={[380000, 440000]}
                i18nStrings={{
                  xTickFormatter: (x: any) => x.toLocaleDateString('en-US', { month: 'short' }),
                  yTickFormatter: (y: number) => `$${(y / 1000).toFixed(0)}k`
                }}
                height={300}
              />
            )}
          </Box>
        </Grid>
      </Container>
    </Layout>
  );
};

export default Dashboard; 