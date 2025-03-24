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
  Select,
  SpaceBetween,
  Cards,
  ColumnLayout
} from '@cloudscape-design/components';
import Layout from '../components/Layout';

interface PropertyDetails {
  address: string;
  price: string;
  bedrooms: string;
  bathrooms: string;
  squareFeet: string;
  propertyType: string;
}

const PropertyAnalysis: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [propertyDetails, setPropertyDetails] = useState<PropertyDetails>({
    address: '',
    price: '',
    bedrooms: '',
    bathrooms: '',
    squareFeet: '',
    propertyType: ''
  });

  const propertyTypes = [
    { label: 'Single Family Home', value: 'single_family' },
    { label: 'Condo', value: 'condo' },
    { label: 'Townhouse', value: 'townhouse' },
    { label: 'Multi-Family', value: 'multi_family' }
  ];

  const handleAnalyze = () => {
    setIsLoading(true);
    // Simulated API call
    setTimeout(() => {
      setShowResults(true);
      setIsLoading(false);
    }, 1500);
  };

  const handleInputChange = (field: keyof PropertyDetails, value: string) => {
    setPropertyDetails(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <Layout activeHref="/property-analysis" isLoading={isLoading}>
      <Container>
        <SpaceBetween size="l">
          <Form
            header={
              <Header
                variant="h2"
                description="Enter property details for analysis"
              >
                Property Details
              </Header>
            }
            actions={
              <Button
                variant="primary"
                onClick={handleAnalyze}
                loading={isLoading}
              >
                Analyze Property
              </Button>
            }
          >
            <Grid
              gridDefinition={[
                { colspan: { default: 6, xxs: 12 } },
                { colspan: { default: 6, xxs: 12 } },
                { colspan: { default: 4, xxs: 12 } },
                { colspan: { default: 4, xxs: 12 } },
                { colspan: { default: 4, xxs: 12 } }
              ]}
            >
              <FormField label="Property Address">
                <Input
                  value={propertyDetails.address}
                  onChange={e => handleInputChange('address', e.detail.value)}
                />
              </FormField>

              <FormField label="Property Type">
                <Select
                  selectedOption={
                    propertyTypes.find(type => type.value === propertyDetails.propertyType) || null
                  }
                  onChange={e => 
                    handleInputChange('propertyType', e.detail.selectedOption?.value || '')
                  }
                  options={propertyTypes}
                />
              </FormField>

              <FormField label="Price">
                <Input
                  type="number"
                  value={propertyDetails.price}
                  onChange={e => handleInputChange('price', e.detail.value)}
                />
              </FormField>

              <FormField label="Bedrooms">
                <Input
                  type="number"
                  value={propertyDetails.bedrooms}
                  onChange={e => handleInputChange('bedrooms', e.detail.value)}
                />
              </FormField>

              <FormField label="Bathrooms">
                <Input
                  type="number"
                  value={propertyDetails.bathrooms}
                  onChange={e => handleInputChange('bathrooms', e.detail.value)}
                />
              </FormField>
            </Grid>
          </Form>

          {showResults && (
            <Container
              header={
                <Header
                  variant="h2"
                  description="Analysis results based on provided details"
                >
                  Analysis Results
                </Header>
              }
            >
              <SpaceBetween size="l">
                <ColumnLayout columns={3}>
                  <Box variant="awsui-key-label">
                    <div>Estimated Value</div>
                    <div>$450,000</div>
                    <div>Based on comparable properties</div>
                  </Box>
                  <Box variant="awsui-key-label">
                    <div>Price per Sq Ft</div>
                    <div>$225</div>
                    <div>Market average: $220</div>
                  </Box>
                  <Box variant="awsui-key-label">
                    <div>Investment Score</div>
                    <div>85/100</div>
                    <div>Strong investment potential</div>
                  </Box>
                </ColumnLayout>

                <Cards
                  cardDefinition={{
                    header: item => item.title,
                    sections: [
                      {
                        id: "details",
                        content: item => item.details
                      },
                      {
                        id: "recommendation",
                        header: "Recommendation",
                        content: item => item.recommendation
                      }
                    ]
                  }}
                  items={[
                    {
                      title: "Market Analysis",
                      details: "Property is in a high-growth area with 5% annual appreciation",
                      recommendation: "Consider long-term hold strategy"
                    },
                    {
                      title: "Rental Potential",
                      details: "Estimated monthly rent: $2,500",
                      recommendation: "Good rental market with low vacancy rates"
                    },
                    {
                      title: "Risk Assessment",
                      details: "Low risk profile based on location and property condition",
                      recommendation: "Proceed with standard due diligence"
                    }
                  ]}
                />
              </SpaceBetween>
            </Container>
          )}
        </SpaceBetween>
      </Container>
    </Layout>
  );
};

export default PropertyAnalysis; 