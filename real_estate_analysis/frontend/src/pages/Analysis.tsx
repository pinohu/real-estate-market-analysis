import React, { useState } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Tab,
  Tabs,
  LinearProgress,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon,
  LocationOn as LocationIcon,
  AttachMoney as MoneyIcon,
} from '@mui/icons-material';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`analysis-tabpanel-${index}`}
      aria-labelledby={`analysis-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const Analysis: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [location, setLocation] = useState('');
  const [propertyType, setPropertyType] = useState('');
  const [priceRange, setPriceRange] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleAnalyze = async () => {
    setIsLoading(true);
    try {
      // TODO: Implement API call for analysis
      await new Promise((resolve) => setTimeout(resolve, 2000)); // Simulated API call
    } catch (error) {
      console.error('Analysis error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const PropertyTypes = [
    'Single Family',
    'Multi Family',
    'Condo',
    'Townhouse',
    'Commercial',
  ];

  const PriceRanges = [
    'Under $100k',
    '$100k - $250k',
    '$250k - $500k',
    '$500k - $1M',
    'Over $1M',
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Market Analysis
      </Typography>

      <Paper sx={{ width: '100%', mb: 2 }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          aria-label="analysis tabs"
        >
          <Tab label="Market Overview" />
          <Tab label="Property Analysis" />
          <Tab label="Investment Opportunities" />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Market Trends
                  </Typography>
                  <Box sx={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Typography color="text.secondary">
                      Market trend chart will be displayed here
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Key Metrics
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Box sx={{ textAlign: 'center' }}>
                        <TrendingUpIcon sx={{ fontSize: 40, color: 'primary.main' }} />
                        <Typography variant="h6">5.2%</Typography>
                        <Typography color="text.secondary">Price Growth</Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={6}>
                      <Box sx={{ textAlign: 'center' }}>
                        <AssessmentIcon sx={{ fontSize: 40, color: 'primary.main' }} />
                        <Typography variant="h6">12</Typography>
                        <Typography color="text.secondary">Days on Market</Typography>
                      </Box>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Property Analysis
                  </Typography>
                  <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel>Location</InputLabel>
                    <Select
                      value={location}
                      label="Location"
                      onChange={(e) => setLocation(e.target.value)}
                    >
                      <MenuItem value="downtown">Downtown</MenuItem>
                      <MenuItem value="suburbs">Suburbs</MenuItem>
                      <MenuItem value="rural">Rural</MenuItem>
                    </Select>
                  </FormControl>
                  <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel>Property Type</InputLabel>
                    <Select
                      value={propertyType}
                      label="Property Type"
                      onChange={(e) => setPropertyType(e.target.value)}
                    >
                      {PropertyTypes.map((type) => (
                        <MenuItem key={type} value={type}>
                          {type}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                  <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel>Price Range</InputLabel>
                    <Select
                      value={priceRange}
                      label="Price Range"
                      onChange={(e) => setPriceRange(e.target.value)}
                    >
                      {PriceRanges.map((range) => (
                        <MenuItem key={range} value={range}>
                          {range}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                  <Button
                    variant="contained"
                    fullWidth
                    onClick={handleAnalyze}
                    disabled={isLoading}
                  >
                    {isLoading ? 'Analyzing...' : 'Analyze Property'}
                  </Button>
                  {isLoading && <LinearProgress sx={{ mt: 2 }} />}
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={8}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Analysis Results
                  </Typography>
                  <Box sx={{ height: 400, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Typography color="text.secondary">
                      Analysis results will be displayed here
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Investment Opportunities
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={4}>
                      <Card variant="outlined">
                        <CardContent>
                          <LocationIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                          <Typography variant="h6">Downtown Condo</Typography>
                          <Typography color="text.secondary">
                            High potential for appreciation
                          </Typography>
                          <Typography variant="h6" color="primary" sx={{ mt: 1 }}>
                            ROI: 8.5%
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={4}>
                      <Card variant="outlined">
                        <CardContent>
                          <MoneyIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                          <Typography variant="h6">Suburban Home</Typography>
                          <Typography color="text.secondary">
                            Stable rental income
                          </Typography>
                          <Typography variant="h6" color="primary" sx={{ mt: 1 }}>
                            ROI: 6.2%
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={4}>
                      <Card variant="outlined">
                        <CardContent>
                          <AssessmentIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                          <Typography variant="h6">Commercial Property</Typography>
                          <Typography color="text.secondary">
                            Long-term investment
                          </Typography>
                          <Typography variant="h6" color="primary" sx={{ mt: 1 }}>
                            ROI: 7.8%
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>
      </Paper>
    </Container>
  );
};

export default Analysis; 