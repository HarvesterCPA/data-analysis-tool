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
} from '@mui/material';
import { Add, Edit, Delete } from '@mui/icons-material';
import { DataGrid, GridColDef, GridActionsCellItem } from '@mui/x-data-grid';
import { incomeService } from '../services/incomeService';
import { IncomeEntry } from '../types';

export const IncomePage: React.FC = () => {
  const [incomeEntries, setIncomeEntries] = useState<IncomeEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [open, setOpen] = useState(false);
  const [editingEntry, setEditingEntry] = useState<IncomeEntry | null>(null);
  const [formData, setFormData] = useState({
    acres_harvested: '',
    rate_per_unit: '',
    total_earned: '',
    client_name: '',
    notes: '',
    harvest_date: new Date().toISOString().split('T')[0],
  });

  useEffect(() => {
    fetchIncomeEntries();
  }, []);

  const fetchIncomeEntries = async () => {
    try {
      const entries = await incomeService.getIncomeEntries();
      setIncomeEntries(entries);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load income entries');
    } finally {
      setLoading(false);
    }
  };

  const handleOpen = (entry?: IncomeEntry) => {
    if (entry) {
      setEditingEntry(entry);
      setFormData({
        acres_harvested: entry.acres_harvested.toString(),
        rate_per_unit: entry.rate_per_unit.toString(),
        total_earned: entry.total_earned.toString(),
        client_name: entry.client_name || '',
        notes: entry.notes || '',
        harvest_date: entry.harvest_date.split('T')[0],
      });
    } else {
      setEditingEntry(null);
      setFormData({
        acres_harvested: '',
        rate_per_unit: '',
        total_earned: '',
        client_name: '',
        notes: '',
        harvest_date: new Date().toISOString().split('T')[0],
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingEntry(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const data = {
        acres_harvested: parseFloat(formData.acres_harvested),
        rate_per_unit: parseFloat(formData.rate_per_unit),
        total_earned: parseFloat(formData.total_earned),
        client_name: formData.client_name || undefined,
        notes: formData.notes || undefined,
        harvest_date: new Date(formData.harvest_date).toISOString(),
      };

      if (editingEntry) {
        await incomeService.updateIncomeEntry(editingEntry.id, data);
      } else {
        await incomeService.createIncomeEntry(data);
      }

      await fetchIncomeEntries();
      handleClose();
    } catch (err: any) {
      console.error('Income creation error:', err);
      if (err.response?.data?.detail) {
        // Handle validation errors
        if (Array.isArray(err.response.data.detail)) {
          setError(err.response.data.detail.map((e: any) => e.msg).join(', '));
        } else {
          setError(err.response.data.detail);
        }
      } else {
        setError('Failed to save income entry');
      }
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this income entry?')) {
      try {
        await incomeService.deleteIncomeEntry(id);
        await fetchIncomeEntries();
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to delete income entry');
      }
    }
  };

  const columns: GridColDef[] = [
    { 
      field: 'harvest_date', 
      headerName: 'Date', 
      width: 120, 
      type: 'date',
      valueGetter: (params) => new Date(params.value)
    },
    { field: 'acres_harvested', headerName: 'Acres', width: 100, type: 'number' },
    { field: 'rate_per_unit', headerName: 'Rate/Unit', width: 120, type: 'number' },
    { field: 'total_earned', headerName: 'Total', width: 120, type: 'number' },
    { field: 'client_name', headerName: 'Client', width: 150 },
    { field: 'notes', headerName: 'Notes', width: 200 },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Actions',
      width: 100,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<Edit />}
          label="Edit"
          onClick={() => handleOpen(params.row)}
        />,
        <GridActionsCellItem
          icon={<Delete />}
          label="Delete"
          onClick={() => handleDelete(params.row.id)}
        />,
      ],
    },
  ];

  const totalIncome = incomeEntries.reduce((sum, entry) => sum + entry.total_earned, 0);

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
        <Typography variant="h4">Income Tracking</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpen()}
        >
          Add Income Entry
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Entries
              </Typography>
              <Typography variant="h4">
                {incomeEntries.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Income
              </Typography>
              <Typography variant="h4">
                ${totalIncome.toLocaleString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Average per Entry
              </Typography>
              <Typography variant="h4">
                ${incomeEntries.length > 0 ? (totalIncome / incomeEntries.length).toLocaleString() : '0'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Acres
              </Typography>
              <Typography variant="h4">
                {incomeEntries.reduce((sum, entry) => sum + entry.acres_harvested, 0).toLocaleString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Card>
        <DataGrid
          rows={incomeEntries}
          columns={columns}
          pageSizeOptions={[5, 10, 25]}
          initialState={{
            pagination: { paginationModel: { pageSize: 10 } },
          }}
          disableRowSelectionOnClick
        />
      </Card>

      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <form onSubmit={handleSubmit}>
          <DialogTitle>
            {editingEntry ? 'Edit Income Entry' : 'Add Income Entry'}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Acres Harvested"
                  type="number"
                  value={formData.acres_harvested}
                  onChange={(e) => setFormData({ ...formData, acres_harvested: e.target.value })}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Rate per Unit"
                  type="number"
                  inputProps={{ step: "0.01" }}
                  value={formData.rate_per_unit}
                  onChange={(e) => setFormData({ ...formData, rate_per_unit: e.target.value })}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Total Earned"
                  type="number"
                  inputProps={{ step: "0.01" }}
                  value={formData.total_earned}
                  onChange={(e) => setFormData({ ...formData, total_earned: e.target.value })}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Harvest Date"
                  type="date"
                  value={formData.harvest_date}
                  onChange={(e) => setFormData({ ...formData, harvest_date: e.target.value })}
                  InputLabelProps={{ shrink: true }}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Client Name"
                  value={formData.client_name}
                  onChange={(e) => setFormData({ ...formData, client_name: e.target.value })}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Notes"
                  multiline
                  rows={3}
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>Cancel</Button>
            <Button type="submit" variant="contained">
              {editingEntry ? 'Update' : 'Add'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};
