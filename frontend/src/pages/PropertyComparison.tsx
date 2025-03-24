import React, { useState } from 'react';
import {
  Container,
  Header,
  Table,
  SpaceBetween,
  Button,
  Input,
  FormField,
  Form,
  ColumnLayout,
  Box,
} from '@cloudscape-design/components';

const PropertyComparison: React.FC = () => {
  const [properties, setProperties] = useState([
    {
      address: '123 Main St',
      price: '$450,000',
      sqft: '2,200',
      bedsBaths: '3/2',
      yearBuilt: '2005',
      pricePerSqft: '$205',
      lotSize: '0.25 acres',
      propertyType: 'Single Family'
    },
    {
      address: '456 Oak Ave',
      price: '$525,000',
      sqft: '2,500',
      bedsBaths: '4/2.5',
      yearBuilt: '2010',
      pricePerSqft: '$210',
      lotSize: '0.3 acres',
      propertyType: 'Single Family'
    }
  ]);

  const [newProperty, setNewProperty] = useState({
    address: '',
    price: '',
    sqft: '',
    bedsBaths: '',
    yearBuilt: '',
    lotSize: '',
    propertyType: ''
  });

  const handleAddProperty = () => {
    const priceNum = parseInt(newProperty.price.replace(/\D/g, ''));
    const sqftNum = parseInt(newProperty.sqft.replace(/\D/g, ''));
    const pricePerSqft = `$${Math.round(priceNum / sqftNum)}`;

    setProperties([...properties, { ...newProperty, pricePerSqft }]);
    setNewProperty({
      address: '',
      price: '',
      sqft: '',
      bedsBaths: '',
      yearBuilt: '',
      lotSize: '',
      propertyType: ''
    });
  };

  return (
    <Container>
      <SpaceBetween size="l">
        <Header
          variant="h1"
          description="Compare multiple properties side by side"
        >
          Property Comparison
        </Header>

        <Form
          header={
            <Header
              variant="h2"
              description="Add a new property to compare"
            >
              Add Property
            </Header>
          }
          actions={
            <Button
              variant="primary"
              onClick={handleAddProperty}
              disabled={!newProperty.address || !newProperty.price || !newProperty.sqft}
            >
              Add Property
            </Button>
          }
        >
          <ColumnLayout columns={3}>
            <FormField label="Address">
              <Input
                value={newProperty.address}
                onChange={e => setNewProperty(prev => ({ ...prev, address: e.detail.value }))}
              />
            </FormField>
            <FormField label="Price">
              <Input
                value={newProperty.price}
                onChange={e => setNewProperty(prev => ({ ...prev, price: e.detail.value }))}
              />
            </FormField>
            <FormField label="Square Feet">
              <Input
                value={newProperty.sqft}
                onChange={e => setNewProperty(prev => ({ ...prev, sqft: e.detail.value }))}
              />
            </FormField>
            <FormField label="Beds/Baths">
              <Input
                value={newProperty.bedsBaths}
                onChange={e => setNewProperty(prev => ({ ...prev, bedsBaths: e.detail.value }))}
              />
            </FormField>
            <FormField label="Year Built">
              <Input
                value={newProperty.yearBuilt}
                onChange={e => setNewProperty(prev => ({ ...prev, yearBuilt: e.detail.value }))}
              />
            </FormField>
            <FormField label="Lot Size">
              <Input
                value={newProperty.lotSize}
                onChange={e => setNewProperty(prev => ({ ...prev, lotSize: e.detail.value }))}
              />
            </FormField>
          </ColumnLayout>
        </Form>

        <Table
          columnDefinitions={[
            {
              id: 'address',
              header: 'Address',
              cell: item => item.address
            },
            {
              id: 'price',
              header: 'Price',
              cell: item => item.price
            },
            {
              id: 'sqft',
              header: 'Square Feet',
              cell: item => item.sqft
            },
            {
              id: 'pricePerSqft',
              header: 'Price/Sq Ft',
              cell: item => item.pricePerSqft
            },
            {
              id: 'bedsBaths',
              header: 'Beds/Baths',
              cell: item => item.bedsBaths
            },
            {
              id: 'yearBuilt',
              header: 'Year Built',
              cell: item => item.yearBuilt
            },
            {
              id: 'lotSize',
              header: 'Lot Size',
              cell: item => item.lotSize
            }
          ]}
          items={properties}
          header={
            <Header
              variant="h2"
              description="Compare property details side by side"
            >
              Property Comparison Table
            </Header>
          }
        />
      </SpaceBetween>
    </Container>
  );
};

export default PropertyComparison; 