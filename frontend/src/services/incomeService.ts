import { api } from './api';
import { IncomeEntry } from '../types';

export const incomeService = {
  async getIncomeEntries(params?: {
    skip?: number;
    limit?: number;
    start_date?: string;
    end_date?: string;
  }): Promise<IncomeEntry[]> {
    const response = await api.get('/api/income/', { params });
    return response.data;
  },

  async getIncomeEntry(id: number): Promise<IncomeEntry> {
    const response = await api.get(`/api/income/${id}`);
    return response.data;
  },

  async createIncomeEntry(data: Omit<IncomeEntry, 'id' | 'user_id' | 'created_at' | 'updated_at'>): Promise<IncomeEntry> {
    const response = await api.post('/api/income/', data);
    return response.data;
  },

  async updateIncomeEntry(id: number, data: Partial<IncomeEntry>): Promise<IncomeEntry> {
    const response = await api.put(`/api/income/${id}`, data);
    return response.data;
  },

  async deleteIncomeEntry(id: number): Promise<void> {
    await api.delete(`/api/income/${id}`);
  },
};
