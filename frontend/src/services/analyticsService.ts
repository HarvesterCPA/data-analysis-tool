import { api } from './api';
import { AnalyticsResponse } from '../types';

export const analyticsService = {
  async getDashboardAnalytics(params?: {
    start_date?: string;
    end_date?: string;
  }): Promise<AnalyticsResponse> {
    const response = await api.get('/api/analytics/dashboard', { params });
    return response.data;
  },
};
