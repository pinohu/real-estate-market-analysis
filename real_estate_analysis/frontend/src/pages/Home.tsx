import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Button,
  Box,
  Card,
  CardContent,
  CardActions,
} from '@mui/material';
import {
  Home as HomeIcon,
  Assessment as AssessmentIcon,
  TrendingUp as TrendingUpIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import { useAuth } from '../hooks/useAuth';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const features = [
    {
      title: 'Property Management',
      description: 'Track and manage your real estate portfolio in one place.',
      icon: <HomeIcon sx={{ fontSize: 40 }} />,
      action: () => navigate('/properties'),
    },
    {
      title: 'Market Analysis',
      description: 'Get insights into market trends and investment opportunities.',
      icon: <AssessmentIcon sx={{ fontSize: 40 }} />,
      action: () => navigate('/analysis'),
    },
    {
      title: 'Investment Tracking',
      description: 'Monitor your investments and track performance metrics.',
      icon: <TrendingUpIcon sx={{ fontSize: 40 }} />,
      action: () => navigate('/portfolio'),
    },
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Welcome Section */}
        <Grid item xs={12}>
          <Paper
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
              color: 'white',
            }}
          >
            <Typography variant="h4" component="h1" gutterBottom>
              Welcome back, {user?.full_name}!
            </Typography>
            <Typography variant="subtitle1" gutterBottom>
              Your real estate investment companion
            </Typography>
            <Button
              variant="contained"
              color="secondary"
              startIcon={<AddIcon />}
              onClick={() => navigate('/properties/new')}
              sx={{ mt: 2 }}
            >
              Add New Property
            </Button>
          </Paper>
        </Grid>

        {/* Features Grid */}
        {features.map((feature, index) => (
          <Grid item xs={12} md={4} key={index}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'scale(1.02)',
                },
              }}
            >
              <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                <Box sx={{ color: 'primary.main', mb: 2 }}>{feature.icon}</Box>
                <Typography gutterBottom variant="h5" component="h2">
                  {feature.title}
                </Typography>
                <Typography color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
              <CardActions sx={{ justifyContent: 'center', pb: 2 }}>
                <Button
                  size="small"
                  color="primary"
                  onClick={feature.action}
                  variant="outlined"
                >
                  Get Started
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}

        {/* Quick Stats */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quick Stats
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={4}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="primary">
                    0
                  </Typography>
                  <Typography color="text.secondary">Total Properties</Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="primary">
                    $0
                  </Typography>
                  <Typography color="text.secondary">Total Investment</Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="primary">
                    0%
                  </Typography>
                  <Typography color="text.secondary">Average ROI</Typography>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Home; 