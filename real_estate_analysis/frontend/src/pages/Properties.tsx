import React, { useState } from 'react';
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
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Chip,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  LocationOn as LocationIcon,
  AttachMoney as MoneyIcon,
  Home as HomeIcon,
} from '@mui/icons-material';
import { useAuth } from '../hooks/useAuth';

interface Property {
  id: number;
  title: string;
  address: string;
  price: number;
  type: string;
  status: string;
  bedrooms: number;
  bathrooms: number;
  squareFeet: number;
}

const PropertyTypes = [
  'Single Family',
  'Multi Family',
  'Condo',
  'Townhouse',
  'Commercial',
];

const PropertyStatus = ['Available', 'Sold', 'Pending', 'Rented'];

const Properties: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [properties, setProperties] = useState<Property[]>([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedProperty, setSelectedProperty] = useState<Property | null>(null);
  const [formData, setFormData] = useState<Partial<Property>>({
    title: '',
    address: '',
    price: 0,
    type: '',
    status: 'Available',
    bedrooms: 0,
    bathrooms: 0,
    squareFeet: 0,
  });

  const handleOpenDialog = (property?: Property) => {
    if (property) {
      setSelectedProperty(property);
      setFormData(property);
    } else {
      setSelectedProperty(null);
      setFormData({
        title: '',
        address: '',
        price: 0,
        type: '',
        status: 'Available',
        bedrooms: 0,
        bathrooms: 0,
        squareFeet: 0,
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedProperty(null);
    setFormData({
      title: '',
      address: '',
      price: 0,
      type: '',
      status: 'Available',
      bedrooms: 0,
      bathrooms: 0,
      squareFeet: 0,
    });
  };

  const handleSubmit = async () => {
    try {
      // TODO: Implement API call to save property
      handleCloseDialog();
      // Refresh properties list
    } catch (error) {
      console.error('Error saving property:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this property?')) {
      try {
        // TODO: Implement API call to delete property
        // Refresh properties list
      } catch (error) {
        console.error('Error deleting property:', error);
      }
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Properties
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Add Property
        </Button>
      </Box>

      <Grid container spacing={3}>
        {properties.map((property) => (
          <Grid item xs={12} sm={6} md={4} key={property.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="h6" component="h2">
                    {property.title}
                  </Typography>
                  <Box>
                    <IconButton
                      size="small"
                      onClick={() => handleOpenDialog(property)}
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => handleDelete(property.id)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <LocationIcon sx={{ mr: 1, color: 'text.secondary' }} />
                  <Typography variant="body2" color="text.secondary">
                    {property.address}
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <MoneyIcon sx={{ mr: 1, color: 'text.secondary' }} />
                  <Typography variant="body2" color="text.secondary">
                    ${property.price.toLocaleString()}
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <HomeIcon sx={{ mr: 1, color: 'text.secondary' }} />
                  <Typography variant="body2" color="text.secondary">
                    {property.bedrooms} beds • {property.bathrooms} baths •{' '}
                    {property.squareFeet.toLocaleString()} sqft
                  </Typography>
                </Box>
                <Chip
                  label={property.status}
                  color={
                    property.status === 'Available'
                      ? 'success'
                      : property.status === 'Pending'
                      ? 'warning'
                      : property.status === 'Sold'
                      ? 'error'
                      : 'default'
                  }
                  size="small"
                  sx={{ mt: 1 }}
                />
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  color="primary"
                  onClick={() => navigate(`/properties/${property.id}`)}
                >
                  View Details
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {selectedProperty ? 'Edit Property' : 'Add New Property'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <TextField
              fullWidth
              label="Title"
              value={formData.title}
              onChange={(e) =>
                setFormData({ ...formData, title: e.target.value })
              }
              margin="normal"
            />
            <TextField
              fullWidth
              label="Address"
              value={formData.address}
              onChange={(e) =>
                setFormData({ ...formData, address: e.target.value })
              }
              margin="normal"
            />
            <TextField
              fullWidth
              label="Price"
              type="number"
              value={formData.price}
              onChange={(e) =>
                setFormData({ ...formData, price: Number(e.target.value) })
              }
              margin="normal"
            />
            <TextField
              fullWidth
              select
              label="Type"
              value={formData.type}
              onChange={(e) =>
                setFormData({ ...formData, type: e.target.value })
              }
              margin="normal"
            >
              {PropertyTypes.map((type) => (
                <MenuItem key={type} value={type}>
                  {type}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              fullWidth
              select
              label="Status"
              value={formData.status}
              onChange={(e) =>
                setFormData({ ...formData, status: e.target.value })
              }
              margin="normal"
            >
              {PropertyStatus.map((status) => (
                <MenuItem key={status} value={status}>
                  {status}
                </MenuItem>
              ))}
            </TextField>
            <Grid container spacing={2}>
              <Grid item xs={4}>
                <TextField
                  fullWidth
                  label="Bedrooms"
                  type="number"
                  value={formData.bedrooms}
                  onChange={(e) =>
                    setFormData({ ...formData, bedrooms: Number(e.target.value) })
                  }
                  margin="normal"
                />
              </Grid>
              <Grid item xs={4}>
                <TextField
                  fullWidth
                  label="Bathrooms"
                  type="number"
                  value={formData.bathrooms}
                  onChange={(e) =>
                    setFormData({ ...formData, bathrooms: Number(e.target.value) })
                  }
                  margin="normal"
                />
              </Grid>
              <Grid item xs={4}>
                <TextField
                  fullWidth
                  label="Square Feet"
                  type="number"
                  value={formData.squareFeet}
                  onChange={(e) =>
                    setFormData({ ...formData, squareFeet: Number(e.target.value) })
                  }
                  margin="normal"
                />
              </Grid>
            </Grid>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained" color="primary">
            {selectedProperty ? 'Update' : 'Add'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Properties; 