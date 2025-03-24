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
  Alert,
  ColumnLayout
} from '@cloudscape-design/components';
import Layout from '../components/Layout';

interface APIKeys {
  censusApiKey: string;
  walkScoreApiKey: string;
  hudApiKey: string;
  dataGovApiKey: string;
  blsApiKey: string;
}

const Settings: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [apiKeys, setApiKeys] = useState<APIKeys>({
    censusApiKey: '',
    walkScoreApiKey: '',
    hudApiKey: '',
    dataGovApiKey: '',
    blsApiKey: ''
  });

  const handleSave = () => {
    setIsLoading(true);
    // Simulated API call to save settings
    setTimeout(() => {
      setShowSuccess(true);
      setIsLoading(false);
      // Hide success message after 3 seconds
      setTimeout(() => setShowSuccess(false), 3000);
    }, 1000);
  };

  const handleInputChange = (field: keyof APIKeys, value: string) => {
    setApiKeys(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <Layout activeHref="/settings" isLoading={isLoading}>
      <Container>
        <SpaceBetween size="l">
          {showSuccess && (
            <Alert
              type="success"
              dismissible
              onDismiss={() => setShowSuccess(false)}
            >
              Settings saved successfully!
            </Alert>
          )}

          <Form
            header={
              <Header
                variant="h2"
                description="Configure your API keys and application settings"
              >
                API Configuration
              </Header>
            }
            actions={
              <Button
                variant="primary"
                onClick={handleSave}
                loading={isLoading}
              >
                Save Settings
              </Button>
            }
          >
            <SpaceBetween size="l">
              <FormField
                label="Census API Key"
                description="Required for demographic data"
              >
                <Input
                  type="password"
                  value={apiKeys.censusApiKey}
                  onChange={e => handleInputChange('censusApiKey', e.detail.value)}
                />
              </FormField>

              <FormField
                label="Walk Score API Key"
                description="Required for walkability metrics"
              >
                <Input
                  type="password"
                  value={apiKeys.walkScoreApiKey}
                  onChange={e => handleInputChange('walkScoreApiKey', e.detail.value)}
                />
              </FormField>

              <FormField
                label="HUD API Key"
                description="Required for housing data"
              >
                <Input
                  type="password"
                  value={apiKeys.hudApiKey}
                  onChange={e => handleInputChange('hudApiKey', e.detail.value)}
                />
              </FormField>

              <FormField
                label="Data.gov API Key"
                description="Required for government data access"
              >
                <Input
                  type="password"
                  value={apiKeys.dataGovApiKey}
                  onChange={e => handleInputChange('dataGovApiKey', e.detail.value)}
                />
              </FormField>

              <FormField
                label="BLS API Key"
                description="Required for employment statistics"
              >
                <Input
                  type="password"
                  value={apiKeys.blsApiKey}
                  onChange={e => handleInputChange('blsApiKey', e.detail.value)}
                />
              </FormField>
            </SpaceBetween>
          </Form>

          <Container
            header={
              <Header
                variant="h2"
                description="Current API status and rate limits"
              >
                API Status
              </Header>
            }
          >
            <ColumnLayout columns={3}>
              <Box variant="awsui-key-label">
                <div>Census API</div>
                <div>Healthy</div>
                <div>Rate Limit: 500/day</div>
              </Box>
              <Box variant="awsui-key-label">
                <div>Walk Score API</div>
                <div>Healthy</div>
                <div>Rate Limit: 1000/day</div>
              </Box>
              <Box variant="awsui-key-label">
                <div>HUD API</div>
                <div>Healthy</div>
                <div>Rate Limit: 100/hour</div>
              </Box>
            </ColumnLayout>
          </Container>
        </SpaceBetween>
      </Container>
    </Layout>
  );
};

export default Settings; 