import { api } from './api';
import { ExpenseEntry } from '../types';

export const expenseService = {
  async getExpenseEntries(params?: {
    skip?: number;
    limit?: number;
    start_date?: string;
    end_date?: string;
    category?: string;
  }): Promise<ExpenseEntry[]> {
    const response = await api.get('/api/expenses/', { params });
    return response.data;
  },

  async getExpenseEntry(id: number): Promise<ExpenseEntry> {
    const response = await api.get(`/api/expenses/${id}`);
    return response.data;
  },

  async createExpenseEntry(data: Omit<ExpenseEntry, 'id' | 'user_id' | 'created_at' | 'updated_at'>): Promise<ExpenseEntry> {
    const response = await api.post('/api/expenses/', data);
    return response.data;
  },

  async updateExpenseEntry(id: number, data: Partial<ExpenseEntry>): Promise<ExpenseEntry> {
    const response = await api.put(`/api/expenses/${id}`, data);
    return response.data;
  },

  async deleteExpenseEntry(id: number): Promise<void> {
    await api.delete(`/api/expenses/${id}`);
  },
};
