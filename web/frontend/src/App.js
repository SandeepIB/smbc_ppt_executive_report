import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Box,
  Alert,
  CircularProgress,
  Card,
  CardContent,

} from '@mui/material';
import { Download, Refresh } from '@mui/icons-material';
import axios from 'axios';
import { API_BASE } from './config';

function App() {
  const [config, setConfig] = useState(null);
  const [slideText, setSlideText] = useState('');
  const [replacements, setReplacements] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/api/config`);
      setConfig(response.data.config);
      setSlideText(response.data.slide_text);
      setReplacements(response.data.config.replacements);
      setError('');
    } catch (err) {
      setError('Failed to load configuration');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (key, value) => {
    setReplacements(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const generateReport = async () => {
    try {
      setLoading(true);
      setError('');
      setSuccess('');
      
      const response = await axios.post(`${API_BASE}/api/generate`, {
        replacements,
        slide_number: config.slide_number
      }, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${new Date().toISOString().slice(0,19).replace(/:/g, '')}.pptx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      setSuccess('Report generated and downloaded successfully!');
    } catch (err) {
      setError('Failed to generate report');
    } finally {
      setLoading(false);
    }
  };

  if (loading && !config) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom align="center" color="primary">
        Automated Executive Report Builder
      </Typography>
      
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Current Slide Content
              </Typography>
              <Paper 
                sx={{ 
                  p: 2, 
                  bgcolor: 'grey.50', 
                  maxHeight: 400, 
                  overflow: 'auto',
                  whiteSpace: 'pre-wrap',
                  fontSize: '0.875rem'
                }}
              >
                {slideText}
              </Paper>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h5">
                  Placeholder Values
                </Typography>
                <Button
                  startIcon={<Refresh />}
                  onClick={loadConfig}
                  disabled={loading}
                >
                  Reset
                </Button>
              </Box>
              
              <Grid container spacing={2}>
                {Object.entries(replacements).map(([key, value]) => (
                  <Grid item xs={12} sm={6} key={key}>
                    <TextField
                      fullWidth
                      label={key}
                      value={value}
                      onChange={(e) => handleInputChange(key, e.target.value)}
                      variant="outlined"
                      size="small"
                    />
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box mt={4} display="flex" justifyContent="center">
        <Button
          variant="contained"
          size="large"
          startIcon={loading ? <CircularProgress size={20} /> : <Download />}
          onClick={generateReport}
          disabled={loading}
          sx={{ px: 4, py: 1.5 }}
        >
          {loading ? 'Generating...' : 'Generate & Download Report'}
        </Button>
      </Box>
    </Container>
  );
}

export default App;