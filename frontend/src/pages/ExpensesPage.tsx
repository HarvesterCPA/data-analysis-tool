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
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import { Add, Edit, Delete } from '@mui/icons-material';
import { DataGrid, GridColDef, GridActionsCellItem } from '@mui/x-data-grid';
import { expenseService } from '../services/expenseService';
import { ExpenseEntry } from '../types';

const EXPENSE_CATEGORIES = [
  { value: 'fuel', label: 'Fuel' },
  { value: 'labor', label: 'Labor' },
  { value: 'equipment_lease', label: 'Equipment Lease' },
  { value: 'equipment_repair', label: 'Equipment Repair' },
  { value: 'equipment_depreciation', label: 'Equipment Depreciation' },
  { value: 'rent_interest', label: 'Rent/Interest' },
  { value: 'taxes', label: 'Taxes' },
  { value: 'other', label: 'Other' },
];

export const ExpensesPage: React.FC = () => {
  const [expenseEntries, setExpenseEntries] = useState<ExpenseEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [open, setOpen] = useState(false);
  const [editingEntry, setEditingEntry] = useState<ExpenseEntry | null>(null);
  const [formData, setFormData] = useState({
    category: 'fuel',
    amount: '',
    description: '',
    notes: '',
    expense_date: new Date().toISOString().split('T')[0],
  });

  useEffect(() => {
    fetchExpenseEntries();
  }, []);

  const fetchExpenseEntries = async () => {
    try {
      const entries = await expenseService.getExpenseEntries();
      setExpenseEntries(entries);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load expense entries');
    } finally {
      setLoading(false);
    }
  };

  const handleOpen = (entry?: ExpenseEntry) => {
    if (entry) {
      setEditingEntry(entry);
      setFormData({
        category: entry.category,
        amount: entry.amount.toString(),
        description: entry.description || '',
        notes: entry.notes || '',
        expense_date: entry.expense_date.split('T')[0],
      });
    } else {
      setEditingEntry(null);
      setFormData({
        category: 'fuel',
        amount: '',
        description: '',
        notes: '',
        expense_date: new Date().toISOString().split('T')[0],
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
        category: formData.category as any,
        amount: parseFloat(formData.amount),
        description: formData.description || undefined,
        notes: formData.notes || undefined,
        expense_date: new Date(formData.expense_date).toISOString(),
      };

      if (editingEntry) {
        await expenseService.updateExpenseEntry(editingEntry.id, data);
      } else {
        await expenseService.createExpenseEntry(data);
      }

      await fetchExpenseEntries();
      handleClose();
    } catch (err: any) {
      console.error('Expense creation error:', err);
      if (err.response?.data?.detail) {
        // Handle validation errors
        if (Array.isArray(err.response.data.detail)) {
          setError(err.response.data.detail.map((e: any) => e.msg).join(', '));
        } else {
          setError(err.response.data.detail);
        }
      } else {
        setError('Failed to save expense entry');
      }
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this expense entry?')) {
      try {
        await expenseService.deleteExpenseEntry(id);
        await fetchExpenseEntries();
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to delete expense entry');
      }
    }
  };

  const columns: GridColDef[] = [
    { 
      field: 'expense_date', 
      headerName: 'Date', 
      width: 120, 
      type: 'date',
      valueGetter: (params) => new Date(params.value)
    },
    { field: 'category', headerName: 'Category', width: 150 },
    { field: 'amount', headerName: 'Amount', width: 120, type: 'number' },
    { field: 'description', headerName: 'Description', width: 200 },
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

  const totalExpenses = expenseEntries.reduce((sum, entry) => sum + entry.amount, 0);
  const categoryTotals = expenseEntries.reduce((acc, entry) => {
    acc[entry.category] = (acc[entry.category] || 0) + entry.amount;
    return acc;
  }, {} as Record<string, number>);

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
        <Typography variant="h4">Expense Tracking</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpen()}
        >
          Add Expense Entry
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
                {expenseEntries.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Expenses
              </Typography>
              <Typography variant="h4">
                ${totalExpenses.toLocaleString()}
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
                ${expenseEntries.length > 0 ? (totalExpenses / expenseEntries.length).toLocaleString() : '0'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Top Category
              </Typography>
              <Typography variant="h6">
                {Object.entries(categoryTotals).sort(([,a], [,b]) => b - a)[0]?.[0] || 'N/A'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Card>
        <DataGrid
          rows={expenseEntries}
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
            {editingEntry ? 'Edit Expense Entry' : 'Add Expense Entry'}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth required>
                  <InputLabel>Category</InputLabel>
                  <Select
                    value={formData.category}
                    label="Category"
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  >
                    {EXPENSE_CATEGORIES.map((category) => (
                      <MenuItem key={category.value} value={category.value}>
                        {category.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Amount"
                  type="number"
                  inputProps={{ step: "0.01" }}
                  value={formData.amount}
                  onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Expense Date"
                  type="date"
                  value={formData.expense_date}
                  onChange={(e) => setFormData({ ...formData, expense_date: e.target.value })}
                  InputLabelProps={{ shrink: true }}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
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
