import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Grid,
  Card,
  CardContent,
  Alert,
  CircularProgress,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import { Add, Edit, Delete, Calculate } from '@mui/icons-material';
import { DataGrid, GridColDef, GridActionsCellItem } from '@mui/x-data-grid';
// Using native HTML date inputs instead of MUI date pickers
import { harvestSeasonService } from '../services/harvestSeasonService';
import { HarvestSeason, PayCycle } from '../types';

export const HarvestSeasonsPage: React.FC = () => {
  const [harvestSeasons, setHarvestSeasons] = useState<HarvestSeason[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [open, setOpen] = useState(false);
  const [editingSeason, setEditingSeason] = useState<HarvestSeason | null>(null);
  const [formData, setFormData] = useState({
    business_name: '',
    business_address: '',
    contact_phone: '',
    contact_email: '',
    estimated_start_date: '',
    estimated_end_date: '',
    actual_start_date: '',
    actual_end_date: '',
    pay_cycle: PayCycle.WEEKLY,
    interest_rate: 6.0,
  });

  useEffect(() => {
    fetchHarvestSeasons();
  }, []);

  const fetchHarvestSeasons = async () => {
    try {
      const seasons = await harvestSeasonService.getHarvestSeasons();
      setHarvestSeasons(seasons);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load harvest seasons');
    } finally {
      setLoading(false);
    }
  };

  const handleOpen = (season?: HarvestSeason) => {
    if (season) {
      setEditingSeason(season);
      setFormData({
        business_name: season.business_name,
        business_address: season.business_address || '',
        contact_phone: season.contact_phone || '',
        contact_email: season.contact_email || '',
        estimated_start_date: season.estimated_start_date ? season.estimated_start_date.split('T')[0] : '',
        estimated_end_date: season.estimated_end_date ? season.estimated_end_date.split('T')[0] : '',
        actual_start_date: season.actual_start_date ? season.actual_start_date.split('T')[0] : '',
        actual_end_date: season.actual_end_date ? season.actual_end_date.split('T')[0] : '',
        pay_cycle: season.pay_cycle,
        interest_rate: season.interest_rate,
      });
    } else {
      setEditingSeason(null);
      setFormData({
        business_name: '',
        business_address: '',
        contact_phone: '',
        contact_email: '',
        estimated_start_date: '',
        estimated_end_date: '',
        actual_start_date: '',
        actual_end_date: '',
        pay_cycle: PayCycle.WEEKLY,
        interest_rate: 6.0,
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingSeason(null);
  };

  const handleSubmit = async () => {
    try {
      if (editingSeason) {
        await harvestSeasonService.updateHarvestSeason(editingSeason.id, formData);
      } else {
        await harvestSeasonService.createHarvestSeason(formData);
      }
      await fetchHarvestSeasons();
      handleClose();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save harvest season');
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this harvest season?')) {
      try {
        await harvestSeasonService.deleteHarvestSeason(id);
        await fetchHarvestSeasons();
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to delete harvest season');
      }
    }
  };

  const handleCalculate = async (id: number) => {
    try {
      await harvestSeasonService.calculateProfitLoss(id);
      setError('');
      // Optionally refresh data or show success message
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to calculate profit/loss');
    }
  };

  const columns: GridColDef[] = [
    { field: 'business_name', headerName: 'Business Name', width: 200 },
    { 
      field: 'pay_cycle', 
      headerName: 'Pay Cycle', 
      width: 120,
      renderCell: (params) => (
        <Chip label={params.value} color="primary" size="small" />
      )
    },
    { field: 'interest_rate', headerName: 'Interest Rate', width: 120, type: 'number' },
    { 
      field: 'estimated_start_date', 
      headerName: 'Est. Start', 
      width: 120, 
      type: 'date',
      valueGetter: (params) => params.value ? new Date(params.value) : null
    },
    { 
      field: 'estimated_end_date', 
      headerName: 'Est. End', 
      width: 120, 
      type: 'date',
      valueGetter: (params) => params.value ? new Date(params.value) : null
    },
    { 
      field: 'actual_start_date', 
      headerName: 'Actual Start', 
      width: 120, 
      type: 'date',
      valueGetter: (params) => params.value ? new Date(params.value) : null
    },
    { 
      field: 'actual_end_date', 
      headerName: 'Actual End', 
      width: 120, 
      type: 'date',
      valueGetter: (params) => params.value ? new Date(params.value) : null
    },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Actions',
      width: 200,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<Edit />}
          label="Edit"
          onClick={() => handleOpen(params.row)}
        />,
        <GridActionsCellItem
          icon={<Calculate />}
          label="Calculate"
          onClick={() => handleCalculate(params.row.id)}
        />,
        <GridActionsCellItem
          icon={<Delete />}
          label="Delete"
          onClick={() => handleDelete(params.row.id)}
        />,
      ],
    },
  ];

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
        <Typography variant="h4">Harvest Seasons</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpen()}
        >
          Add Harvest Season
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Card>
        <CardContent>
          <DataGrid
            rows={harvestSeasons}
            columns={columns}
            pageSizeOptions={[5, 10, 25]}
            initialState={{
              pagination: { paginationModel: { pageSize: 10 } },
            }}
            disableRowSelectionOnClick
          />
        </CardContent>
      </Card>

      <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingSeason ? 'Edit Harvest Season' : 'Add Harvest Season'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Business Name"
                value={formData.business_name}
                onChange={(e) => setFormData({ ...formData, business_name: e.target.value })}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Business Address"
                value={formData.business_address}
                onChange={(e) => setFormData({ ...formData, business_address: e.target.value })}
                multiline
                rows={2}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Contact Phone"
                value={formData.contact_phone}
                onChange={(e) => setFormData({ ...formData, contact_phone: e.target.value })}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Contact Email"
                value={formData.contact_email}
                onChange={(e) => setFormData({ ...formData, contact_email: e.target.value })}
                type="email"
              />
            </Grid>
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>Pay Cycle</InputLabel>
                <Select
                  value={formData.pay_cycle}
                  onChange={(e) => setFormData({ ...formData, pay_cycle: e.target.value as PayCycle })}
                >
                  <MenuItem value={PayCycle.WEEKLY}>Weekly</MenuItem>
                  <MenuItem value={PayCycle.BI_WEEKLY}>Bi-Weekly</MenuItem>
                  <MenuItem value={PayCycle.SEMI_MONTHLY}>Semi-Monthly</MenuItem>
                  <MenuItem value={PayCycle.MONTHLY}>Monthly</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Interest Rate (%)"
                type="number"
                value={formData.interest_rate}
                onChange={(e) => setFormData({ ...formData, interest_rate: parseFloat(e.target.value) })}
                inputProps={{ min: 0, max: 100, step: 0.1 }}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Estimated Start Date"
                type="date"
                value={formData.estimated_start_date}
                onChange={(e) => setFormData({ ...formData, estimated_start_date: e.target.value })}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Estimated End Date"
                type="date"
                value={formData.estimated_end_date}
                onChange={(e) => setFormData({ ...formData, estimated_end_date: e.target.value })}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Actual Start Date"
                type="date"
                value={formData.actual_start_date}
                onChange={(e) => setFormData({ ...formData, actual_start_date: e.target.value })}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Actual End Date"
                type="date"
                value={formData.actual_end_date}
                onChange={(e) => setFormData({ ...formData, actual_end_date: e.target.value })}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingSeason ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
