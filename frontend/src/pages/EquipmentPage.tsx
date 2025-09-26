import React, { useState, useEffect, useCallback } from 'react';
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
import { equipmentService } from '../services/equipmentService';
import { Equipment, EquipmentType, OwnershipType } from '../types';

interface EquipmentPageProps {
  harvestSeasonId: number;
}

export const EquipmentPage: React.FC<EquipmentPageProps> = ({ harvestSeasonId }) => {
  const [equipment, setEquipment] = useState<Equipment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [open, setOpen] = useState(false);
  const [editingEquipment, setEditingEquipment] = useState<Equipment | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    equipment_type: EquipmentType.COMBINE,
    ownership_type: OwnershipType.OWNED,
    purchase_date: '',
    purchase_price: '',
    current_value: '',
    years_ownership: '',
    lease_rate: '',
    finance_rate: '',
    down_payment: '',
    monthly_payment: '',
    working_days: '',
  });

  const fetchEquipment = useCallback(async () => {
    try {
      const equipmentList = await equipmentService.getEquipmentByHarvestSeason(harvestSeasonId);
      setEquipment(equipmentList);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load equipment');
    } finally {
      setLoading(false);
    }
  }, [harvestSeasonId]);

  useEffect(() => {
    fetchEquipment();
  }, [fetchEquipment]);

  const handleOpen = (equipmentItem?: Equipment) => {
    if (equipmentItem) {
      setEditingEquipment(equipmentItem);
      setFormData({
        name: equipmentItem.name,
        equipment_type: equipmentItem.equipment_type,
        ownership_type: equipmentItem.ownership_type,
        purchase_date: equipmentItem.purchase_date ? equipmentItem.purchase_date.split('T')[0] : '',
        purchase_price: equipmentItem.purchase_price?.toString() || '',
        current_value: equipmentItem.current_value?.toString() || '',
        years_ownership: equipmentItem.years_ownership?.toString() || '',
        lease_rate: equipmentItem.lease_rate?.toString() || '',
        finance_rate: equipmentItem.finance_rate?.toString() || '',
        down_payment: equipmentItem.down_payment?.toString() || '',
        monthly_payment: equipmentItem.monthly_payment?.toString() || '',
        working_days: equipmentItem.working_days?.toString() || '',
      });
    } else {
      setEditingEquipment(null);
      setFormData({
        name: '',
        equipment_type: EquipmentType.COMBINE,
        ownership_type: OwnershipType.OWNED,
        purchase_date: '',
        purchase_price: '',
        current_value: '',
        years_ownership: '',
        lease_rate: '',
        finance_rate: '',
        down_payment: '',
        monthly_payment: '',
        working_days: '',
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingEquipment(null);
  };

  const handleSubmit = async () => {
    try {
      const submitData = {
        ...formData,
        harvest_season_id: harvestSeasonId,
        purchase_date: formData.purchase_date || undefined,
        purchase_price: formData.purchase_price ? parseFloat(formData.purchase_price) : undefined,
        current_value: formData.current_value ? parseFloat(formData.current_value) : undefined,
        years_ownership: formData.years_ownership ? parseFloat(formData.years_ownership) : undefined,
        lease_rate: formData.lease_rate ? parseFloat(formData.lease_rate) : undefined,
        finance_rate: formData.finance_rate ? parseFloat(formData.finance_rate) : undefined,
        down_payment: formData.down_payment ? parseFloat(formData.down_payment) : undefined,
        monthly_payment: formData.monthly_payment ? parseFloat(formData.monthly_payment) : undefined,
        working_days: formData.working_days ? parseFloat(formData.working_days) : undefined,
      };

      if (editingEquipment) {
        await equipmentService.updateEquipment(editingEquipment.id, submitData);
      } else {
        await equipmentService.createEquipment(submitData);
      }
      await fetchEquipment();
      handleClose();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save equipment');
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this equipment?')) {
      try {
        await equipmentService.deleteEquipment(id);
        await fetchEquipment();
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to delete equipment');
      }
    }
  };

  const handleCalculate = async (id: number) => {
    try {
      await equipmentService.calculateEquipmentCosts(id);
      setError('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to calculate equipment costs');
    }
  };

  const columns: GridColDef[] = [
    { field: 'name', headerName: 'Name', width: 150 },
    { 
      field: 'equipment_type', 
      headerName: 'Type', 
      width: 120,
      renderCell: (params) => (
        <Chip label={params.value} color="primary" size="small" />
      )
    },
    { 
      field: 'ownership_type', 
      headerName: 'Ownership', 
      width: 120,
      renderCell: (params) => (
        <Chip label={params.value} color="secondary" size="small" />
      )
    },
    { field: 'purchase_price', headerName: 'Purchase Price', width: 130, type: 'number' },
    { field: 'current_value', headerName: 'Current Value', width: 130, type: 'number' },
    { field: 'working_days', headerName: 'Working Days', width: 120, type: 'number' },
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
        <Typography variant="h4">Equipment</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpen()}
        >
          Add Equipment
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
            rows={equipment}
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
          {editingEquipment ? 'Edit Equipment' : 'Add Equipment'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Equipment Name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
              />
            </Grid>
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>Equipment Type</InputLabel>
                <Select
                  value={formData.equipment_type}
                  onChange={(e) => setFormData({ ...formData, equipment_type: e.target.value as EquipmentType })}
                >
                  {Object.values(EquipmentType).map((type) => (
                    <MenuItem key={type} value={type}>
                      {type.replace('_', ' ').toUpperCase()}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>Ownership Type</InputLabel>
                <Select
                  value={formData.ownership_type}
                  onChange={(e) => setFormData({ ...formData, ownership_type: e.target.value as OwnershipType })}
                >
                  {Object.values(OwnershipType).map((type) => (
                    <MenuItem key={type} value={type}>
                      {type.replace('_', ' ').toUpperCase()}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Purchase Date"
                type="date"
                value={formData.purchase_date}
                onChange={(e) => setFormData({ ...formData, purchase_date: e.target.value })}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Working Days"
                type="number"
                value={formData.working_days}
                onChange={(e) => setFormData({ ...formData, working_days: e.target.value })}
                inputProps={{ min: 0 }}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Purchase Price"
                type="number"
                value={formData.purchase_price}
                onChange={(e) => setFormData({ ...formData, purchase_price: e.target.value })}
                inputProps={{ min: 0, step: 0.01 }}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Current Value"
                type="number"
                value={formData.current_value}
                onChange={(e) => setFormData({ ...formData, current_value: e.target.value })}
                inputProps={{ min: 0, step: 0.01 }}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Years of Ownership"
                type="number"
                value={formData.years_ownership}
                onChange={(e) => setFormData({ ...formData, years_ownership: e.target.value })}
                inputProps={{ min: 0, step: 0.1 }}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Lease Rate (Monthly)"
                type="number"
                value={formData.lease_rate}
                onChange={(e) => setFormData({ ...formData, lease_rate: e.target.value })}
                inputProps={{ min: 0, step: 0.01 }}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Finance Rate (Annual %)"
                type="number"
                value={formData.finance_rate}
                onChange={(e) => setFormData({ ...formData, finance_rate: e.target.value })}
                inputProps={{ min: 0, max: 100, step: 0.1 }}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Monthly Payment"
                type="number"
                value={formData.monthly_payment}
                onChange={(e) => setFormData({ ...formData, monthly_payment: e.target.value })}
                inputProps={{ min: 0, step: 0.01 }}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingEquipment ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
