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
  ColumnLayout,
  Cards
} from '@cloudscape-design/components';

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
    {
      neighborhood: 'Downtown',
      medianPrice: '$525,000',
      priceChange: '+6.2%',
      inventory: '145',
      daysOnMarket: '25'
    },
    {
      neighborhood: 'Suburbs North',
      medianPrice: '$425,000',
      priceChange: '+4.8%',
      inventory: '230',
      daysOnMarket: '32'
    },
    {
      neighborhood: 'Suburbs South',
      medianPrice: '$395,000',
      priceChange: '+5.1%',
      inventory: '185',
      daysOnMarket: '28'
    }
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
    <Container>
      <SpaceBetween size="l">
        <Header
          variant="h1"
          description="Detailed analysis of market trends by neighborhood"
        >
          Market Analysis
        </Header>

        <Table
          columnDefinitions={[
            {
              id: 'neighborhood',
              header: 'Neighborhood',
              cell: item => item.neighborhood
            },
            {
              id: 'medianPrice',
              header: 'Median Price',
              cell: item => item.medianPrice
            },
            {
              id: 'priceChange',
              header: 'YoY Change',
              cell: item => (
                <Box color={item.priceChange.startsWith('+') ? 'text-status-success' : 'text-status-error'}>
                  {item.priceChange}
                </Box>
              )
            },
            {
              id: 'inventory',
              header: 'Active Listings',
              cell: item => item.inventory
            },
            {
              id: 'daysOnMarket',
              header: 'Days on Market',
              cell: item => item.daysOnMarket
            }
          ]}
          items={marketTrends}
          header={
            <Header
              variant="h2"
              description="Current market metrics by neighborhood"
            >
              Neighborhood Trends
            </Header>
          }
        />

        <Cards
          cardDefinition={{
            header: item => (
              <Header variant="h3">{item.neighborhood}</Header>
            ),
            sections: [
              {
                id: 'metrics',
                content: item => (
                  <ColumnLayout columns={2} variant="text-grid">
                    <div>
                      <Box variant="awsui-key-label">Median Price</Box>
                      <Box variant="p">{item.medianPrice}</Box>
                    </div>
                    <div>
                      <Box variant="awsui-key-label">Price Change</Box>
                      <Box variant="p" color={item.priceChange.startsWith('+') ? 'text-status-success' : 'text-status-error'}>
                        {item.priceChange}
                      </Box>
                    </div>
                    <div>
                      <Box variant="awsui-key-label">Active Listings</Box>
                      <Box variant="p">{item.inventory}</Box>
                    </div>
                    <div>
                      <Box variant="awsui-key-label">Days on Market</Box>
                      <Box variant="p">{item.daysOnMarket}</Box>
                    </div>
                  </ColumnLayout>
                )
              }
            ]
          }}
          items={marketTrends}
          header={
            <Header
              variant="h2"
              description="Detailed view of each neighborhood"
            >
              Neighborhood Cards
            </Header>
          }
        />
      </SpaceBetween>
    </Container>
  );
};

export default MarketAnalysis; 