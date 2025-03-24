import React, { useState } from 'react';
import {
  Box,
  Button,
  Container,
  Form,
  FormField,
  Grid,
  Header,
  Input,
  SpaceBetween,
  Table,
  LineChart,
  ColumnLayout
} from '@cloudscape-design/components';
import Layout from '../components/Layout';

interface MarketMetrics {
  medianPrice: string;
  inventory: string;
  daysOnMarket: string;
  pricePerSqFt: string;
  yearOverYearChange: string;
}

const MarketAnalysis: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [location, setLocation] = useState({
    city: '',
    state: '',
    zipCode: ''
  });

  const handleAnalyze = () => {
    setIsLoading(true);
    // Simulated API call
    setTimeout(() => {
      setShowResults(true);
      setIsLoading(false);
    }, 1500);
  };

  const marketTrends = [
    { month: new Date('2023-01'), value: 425000 },
    { month: new Date('2023-02'), value: 430000 },
    { month: new Date('2023-03'), value: 435000 },
    { month: new Date('2023-04'), value: 440000 },
    { month: new Date('2023-05'), value: 445000 },
    { month: new Date('2023-06'), value: 450000 }
  ];

  const comparableProperties = [
    {
      address: '123 Oak St',
      price: '$445,000',
      sqft: '2,200',
      bedsBaths: '3/2',
      daysOnMarket: '15'
    },
    {
      address: '456 Maple Ave',
      price: '$452,000',
      sqft: '2,300',
      bedsBaths: '3/2.5',
      daysOnMarket: '22'
    },
    {
      address: '789 Pine Rd',
      price: '$438,000',
      sqft: '2,100',
      bedsBaths: '3/2',
      daysOnMarket: '30'
    }
  ];

  return (
    <Layout activeHref="/market-analysis" isLoading={isLoading}>
      <Container>
        <SpaceBetween size="l">
          <Form
            header={
              <Header
                variant="h2"
                description="Enter location details for market analysis"
              >
                Market Location
              </Header>
            }
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
            <Grid
              gridDefinition={[
                { colspan: { default: 4, xxs: 12 } },
                { colspan: { default: 4, xxs: 12 } },
                { colspan: { default: 4, xxs: 12 } }
              ]}
            >
              <FormField label="City">
                <Input
                  value={location.city}
                  onChange={e => setLocation(prev => ({ ...prev, city: e.detail.value }))}
                />
              </FormField>

              <FormField label="State">
                <Input
                  value={location.state}
                  onChange={e => setLocation(prev => ({ ...prev, state: e.detail.value }))}
                />
              </FormField>

              <FormField label="ZIP Code">
                <Input
                  value={location.zipCode}
                  onChange={e => setLocation(prev => ({ ...prev, zipCode: e.detail.value }))}
                />
              </FormField>
            </Grid>
          </Form>

          {showResults && (
            <>
              <Container
                header={
                  <Header
                    variant="h2"
                    description="Current market metrics"
                  >
                    Market Overview
                  </Header>
                }
              >
                <ColumnLayout columns={4}>
                  <Box variant="awsui-key-label">
                    <div>Median Price</div>
                    <div>$450,000</div>
                    <div>↑ 5.2% YoY</div>
                  </Box>
                  <Box variant="awsui-key-label">
                    <div>Inventory</div>
                    <div>245</div>
                    <div>↓ 12% YoY</div>
                  </Box>
                  <Box variant="awsui-key-label">
                    <div>Days on Market</div>
                    <div>22</div>
                    <div>↓ 8 days YoY</div>
                  </Box>
                  <Box variant="awsui-key-label">
                    <div>Price per Sq Ft</div>
                    <div>$225</div>
                    <div>↑ 4.8% YoY</div>
                  </Box>
                </ColumnLayout>
              </Container>

              <Container
                header={
                  <Header
                    variant="h2"
                    description="6-month price trend"
                  >
                    Market Trends
                  </Header>
                }
              >
                <LineChart
                  series={[
                    {
                      title: "Median Price",
                      type: "line",
                      data: marketTrends.map(trend => ({
                        x: trend.month,
                        y: trend.value
                      }))
                    }
                  ]}
                  xDomain={[marketTrends[0].month, marketTrends[marketTrends.length - 1].month]}
                  yDomain={[400000, 475000]}
                  i18nStrings={{
                    xTickFormatter: (x: Date) => x.toLocaleDateString('en-US', { month: 'short' }),
                    yTickFormatter: (y: number) => `$${(y / 1000).toFixed(0)}k`
                  }}
                  height={300}
                />
              </Container>

              <Container
                header={
                  <Header
                    variant="h2"
                    description="Recent comparable properties in the area"
                  >
                    Comparable Properties
                  </Header>
                }
              >
                <Table
                  columnDefinitions={[
                    {
                      id: "address",
                      header: "Address",
                      cell: item => item.address
                    },
                    {
                      id: "price",
                      header: "Price",
                      cell: item => item.price
                    },
                    {
                      id: "sqft",
                      header: "Square Feet",
                      cell: item => item.sqft
                    },
                    {
                      id: "bedsBaths",
                      header: "Beds/Baths",
                      cell: item => item.bedsBaths
                    },
                    {
                      id: "daysOnMarket",
                      header: "Days on Market",
                      cell: item => item.daysOnMarket
                    }
                  ]}
                  items={comparableProperties}
                  loading={isLoading}
                  loadingText="Loading comparable properties"
                  variant="embedded"
                />
              </Container>
            </>
          )}
        </SpaceBetween>
      </Container>
    </Layout>
  );
};

export default MarketAnalysis; 