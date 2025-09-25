import React from 'react';
import {
  Container,
  Typography,
  Card,
  CardContent,
  Grid,
  Box,
  Alert,
  Button,
  Paper,
} from '@mui/material';
import {
  Dashboard,
  AttachMoney,
  Receipt,
  TrendingUp,
  TrendingDown,
} from '@mui/icons-material';

export const DemoPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h3" gutterBottom align="center" color="primary">
        🌾 Harvester Tracking Platform
      </Typography>
      
      <Alert severity="info" sx={{ mb: 4 }}>
        <Typography variant="h6">Demo Mode</Typography>
        <Typography>
          This is a frontend demo. To see full functionality, install Python and Docker, 
          then run the complete setup.
        </Typography>
      </Alert>

      <Grid container spacing={3}>
        {/* Dashboard Overview */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                📊 Dashboard Overview
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={3}>
                  <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'success.light' }}>
                    <AttachMoney color="primary" sx={{ fontSize: 40 }} />
                    <Typography variant="h4">$25,000</Typography>
                    <Typography color="textSecondary">Total Income</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'error.light' }}>
                    <Receipt color="error" sx={{ fontSize: 40 }} />
                    <Typography variant="h4">$18,500</Typography>
                    <Typography color="textSecondary">Total Expenses</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'success.light' }}>
                    <TrendingUp color="success" sx={{ fontSize: 40 }} />
                    <Typography variant="h4">$6,500</Typography>
                    <Typography color="textSecondary">Profit</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'info.light' }}>
                    <Dashboard color="info" sx={{ fontSize: 40 }} />
                    <Typography variant="h4">85%</Typography>
                    <Typography color="textSecondary">Efficiency</Typography>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Features */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                ✨ Key Features
              </Typography>
              <Box component="ul" sx={{ pl: 2 }}>
                <li>Track income and expenses</li>
                <li>Peer comparisons (state & national)</li>
                <li>Profit/loss analytics</li>
                <li>Expense categorization</li>
                <li>Dashboard with insights</li>
                <li>Admin panel</li>
                <li>Secure authentication</li>
                <li>Mobile responsive design</li>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🚀 Getting Started
              </Typography>
              <Typography paragraph>
                To run the complete application:
              </Typography>
              <Box component="ol" sx={{ pl: 2 }}>
                <li>Install Python 3.8+</li>
                <li>Install Docker Desktop</li>
                <li>Run <code>setup.bat</code></li>
                <li>Access at http://localhost:3000</li>
              </Box>
              <Button 
                variant="contained" 
                href="https://www.python.org/downloads/" 
                target="_blank"
                sx={{ mr: 1 }}
              >
                Install Python
              </Button>
              <Button 
                variant="contained" 
                href="https://www.docker.com/products/docker-desktop/" 
                target="_blank"
              >
                Install Docker
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Tech Stack */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🛠️ Technology Stack
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={3}>
                  <Paper sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h6" color="primary">Backend</Typography>
                    <Typography>FastAPI + Python</Typography>
                    <Typography>PostgreSQL Database</Typography>
                    <Typography>JWT Authentication</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Paper sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h6" color="primary">Frontend</Typography>
                    <Typography>React + TypeScript</Typography>
                    <Typography>Material-UI</Typography>
                    <Typography>Responsive Design</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Paper sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h6" color="primary">DevOps</Typography>
                    <Typography>Docker Compose</Typography>
                    <Typography>Database Migrations</Typography>
                    <Typography>Environment Config</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Paper sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h6" color="primary">Features</Typography>
                    <Typography>Real-time Analytics</Typography>
                    <Typography>Peer Comparisons</Typography>
                    <Typography>Admin Dashboard</Typography>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};
