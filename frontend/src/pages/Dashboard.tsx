import React from 'react';
import {
  Cards,
  Container,
  Header,
  Box,
  ColumnLayout,
} from '@cloudscape-design/components';

const Dashboard: React.FC = () => {
  const marketMetrics = [
    {
      title: 'Average Price',
      value: '$450,000',
      trend: '+5.2%',
      period: 'vs last month'
    },
    {
      title: 'Days on Market',
      value: '28',
      trend: '-3.1%',
      period: 'vs last month'
    },
    {
      title: 'Active Listings',
      value: '1,245',
      trend: '+12.4%',
      period: 'vs last month'
    },
    {
      title: 'Price per Sq Ft',
      value: '$225',
      trend: '+4.8%',
      period: 'vs last month'
    }
  ];

  return (
    <Container>
      <Header
        variant="h1"
        description="Overview of the current real estate market"
      >
        Market Dashboard
      </Header>
      
      <ColumnLayout columns={2} variant="text-grid">
        {marketMetrics.map((metric, index) => (
          <Box
            key={index}
            padding="l"
            textAlign="center"
            variant="awsui-key-label"
          >
            <Box variant="h2">{metric.title}</Box>
            <Box variant="h1" padding="s">
              {metric.value}
            </Box>
            <Box color={metric.trend.startsWith('+') ? 'text-status-success' : 'text-status-error'}>
              {metric.trend} {metric.period}
            </Box>
          </Box>
        ))}
      </ColumnLayout>
    </Container>
  );
};

export default Dashboard; 