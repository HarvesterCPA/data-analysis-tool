import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Alert,
  CircularProgress,
  Button,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import { Calculate, Download } from '@mui/icons-material';
import { summaryService } from '../services/summaryService';
import { ProfitLossSummary, CostBreakdown, RevenueBreakdown, EquipmentAnalysis } from '../types';

interface HarvestSummaryPageProps {
  harvestSeasonId: number;
}

export const HarvestSummaryPage: React.FC<HarvestSummaryPageProps> = ({ harvestSeasonId }) => {
  const [profitLoss, setProfitLoss] = useState<ProfitLossSummary | null>(null);
  const [costBreakdown, setCostBreakdown] = useState<CostBreakdown | null>(null);
  const [revenueBreakdown, setRevenueBreakdown] = useState<RevenueBreakdown | null>(null);
  const [equipmentAnalysis, setEquipmentAnalysis] = useState<EquipmentAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  const fetchSummaryData = useCallback(async () => {
    try {
      const [profitLossData, costData, revenueData, equipmentData] = await Promise.all([
        summaryService.getProfitLossSummary(harvestSeasonId),
        summaryService.getCostBreakdown(harvestSeasonId),
        summaryService.getRevenueBreakdown(harvestSeasonId),
        summaryService.getEquipmentAnalysis(harvestSeasonId),
      ]);

      setProfitLoss(profitLossData);
      setCostBreakdown(costData);
      setRevenueBreakdown(revenueData);
      setEquipmentAnalysis(equipmentData);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load summary data');
    } finally {
      setLoading(false);
    }
  }, [harvestSeasonId]);

  useEffect(() => {
    fetchSummaryData();
  }, [fetchSummaryData]);

  const handleRecalculate = async () => {
    try {
      await summaryService.recalculateSummary(harvestSeasonId);
      await fetchSummaryData();
      setError('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to recalculate summary');
    }
  };

  const handleExport = () => {
    // TODO: Implement data export functionality
    console.log('Export functionality to be implemented');
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Harvest Summary</Typography>
        <Box>
          <Button
            variant="outlined"
            startIcon={<Calculate />}
            onClick={handleRecalculate}
            sx={{ mr: 2 }}
          >
            Recalculate
          </Button>
          <Button
            variant="contained"
            startIcon={<Download />}
            onClick={handleExport}
          >
            Export Data
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Profit/Loss Summary */}
      {profitLoss && (
        <Grid container spacing={3} mb={3}>
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Total Revenue
                </Typography>
                <Typography variant="h4" color="success.main">
                  ${profitLoss.total_revenue.toLocaleString()}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Total Expenses
                </Typography>
                <Typography variant="h4" color="error.main">
                  ${profitLoss.total_expenses.toLocaleString()}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Net Profit
                </Typography>
                <Typography 
                  variant="h4" 
                  color={profitLoss.net_profit >= 0 ? "success.main" : "error.main"}
                >
                  ${profitLoss.net_profit.toLocaleString()}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Profit Margin
                </Typography>
                <Typography 
                  variant="h4" 
                  color={profitLoss.profit_margin >= 0 ? "success.main" : "error.main"}
                >
                  {profitLoss.profit_margin.toFixed(1)}%
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Per-Acre Analysis */}
      {profitLoss && (
        <Grid container spacing={3} mb={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Cost per Acre
                </Typography>
                <Typography variant="h5">
                  ${profitLoss.cost_per_acre.toFixed(2)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Revenue per Acre
                </Typography>
                <Typography variant="h5">
                  ${profitLoss.revenue_per_acre.toFixed(2)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Profit per Acre
                </Typography>
                <Typography 
                  variant="h5" 
                  color={profitLoss.profit_per_acre >= 0 ? "success.main" : "error.main"}
                >
                  ${profitLoss.profit_per_acre.toFixed(2)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Cost Breakdown */}
      {costBreakdown && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Cost Breakdown
            </Typography>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Category</TableCell>
                    <TableCell align="right">Amount</TableCell>
                    <TableCell align="right">Percentage</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  <TableRow>
                    <TableCell>Equipment</TableCell>
                    <TableCell align="right">${costBreakdown.equipment_cost.toLocaleString()}</TableCell>
                    <TableCell align="right">
                      {((costBreakdown.equipment_cost / costBreakdown.total_cost) * 100).toFixed(1)}%
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Housing</TableCell>
                    <TableCell align="right">${costBreakdown.housing_cost.toLocaleString()}</TableCell>
                    <TableCell align="right">
                      {((costBreakdown.housing_cost / costBreakdown.total_cost) * 100).toFixed(1)}%
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Employees</TableCell>
                    <TableCell align="right">${costBreakdown.employee_cost.toLocaleString()}</TableCell>
                    <TableCell align="right">
                      {((costBreakdown.employee_cost / costBreakdown.total_cost) * 100).toFixed(1)}%
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Fuel</TableCell>
                    <TableCell align="right">${costBreakdown.fuel_cost.toLocaleString()}</TableCell>
                    <TableCell align="right">
                      {((costBreakdown.fuel_cost / costBreakdown.total_cost) * 100).toFixed(1)}%
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Maintenance</TableCell>
                    <TableCell align="right">${costBreakdown.maintenance_cost.toLocaleString()}</TableCell>
                    <TableCell align="right">
                      {((costBreakdown.maintenance_cost / costBreakdown.total_cost) * 100).toFixed(1)}%
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Insurance</TableCell>
                    <TableCell align="right">${costBreakdown.insurance_cost.toLocaleString()}</TableCell>
                    <TableCell align="right">
                      {((costBreakdown.insurance_cost / costBreakdown.total_cost) * 100).toFixed(1)}%
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Taxes</TableCell>
                    <TableCell align="right">${costBreakdown.tax_cost.toLocaleString()}</TableCell>
                    <TableCell align="right">
                      {((costBreakdown.tax_cost / costBreakdown.total_cost) * 100).toFixed(1)}%
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Other</TableCell>
                    <TableCell align="right">${costBreakdown.other_cost.toLocaleString()}</TableCell>
                    <TableCell align="right">
                      {((costBreakdown.other_cost / costBreakdown.total_cost) * 100).toFixed(1)}%
                    </TableCell>
                  </TableRow>
                  <TableRow sx={{ fontWeight: 'bold' }}>
                    <TableCell>Total</TableCell>
                    <TableCell align="right">${costBreakdown.total_cost.toLocaleString()}</TableCell>
                    <TableCell align="right">100%</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      )}

      {/* Revenue Breakdown */}
      {revenueBreakdown && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Revenue Breakdown
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Typography variant="h5" color="success.main">
                  Total Revenue: ${revenueBreakdown.total_revenue.toLocaleString()}
                </Typography>
                <Typography variant="h6" sx={{ mt: 1 }}>
                  Revenue per Acre: ${revenueBreakdown.revenue_per_acre.toFixed(2)}
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1" gutterBottom>
                  Revenue by Crop:
                </Typography>
                {Object.entries(revenueBreakdown.revenue_by_crop).map(([crop, amount]) => (
                  <Chip
                    key={crop}
                    label={`${crop}: $${amount.toLocaleString()}`}
                    color="primary"
                    sx={{ mr: 1, mb: 1 }}
                  />
                ))}
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}

      {/* Equipment Analysis */}
      {equipmentAnalysis && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Equipment Cost Analysis
            </Typography>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Equipment</TableCell>
                    <TableCell align="right">Total Cost</TableCell>
                    <TableCell align="right">Cost per Acre</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {Object.entries(equipmentAnalysis.equipment_cost_breakdown).map(([equipment, cost]) => (
                    <TableRow key={equipment}>
                      <TableCell>{equipment}</TableCell>
                      <TableCell align="right">${cost.toLocaleString()}</TableCell>
                      <TableCell align="right">
                        ${equipmentAnalysis.cost_per_acre_by_equipment[equipment]?.toFixed(2) || '0.00'}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};
