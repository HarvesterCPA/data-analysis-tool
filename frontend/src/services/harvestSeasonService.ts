import { api } from './api';
import { HarvestSeason } from '../types';

export const harvestSeasonService = {
  async getHarvestSeasons(): Promise<HarvestSeason[]> {
    const response = await api.get('/api/harvest-seasons/');
    return response.data;
  },

  async getHarvestSeason(id: number): Promise<HarvestSeason> {
    const response = await api.get(`/api/harvest-seasons/${id}`);
    return response.data;
  },

  async createHarvestSeason(data: Partial<HarvestSeason>): Promise<HarvestSeason> {
    const response = await api.post('/api/harvest-seasons/', data);
    return response.data;
  },

  async updateHarvestSeason(id: number, data: Partial<HarvestSeason>): Promise<HarvestSeason> {
    const response = await api.put(`/api/harvest-seasons/${id}`, data);
    return response.data;
  },

  async deleteHarvestSeason(id: number): Promise<void> {
    await api.delete(`/api/harvest-seasons/${id}`);
  },

  async calculateProfitLoss(id: number): Promise<void> {
    await api.post(`/api/harvest-seasons/${id}/calculate`);
  },
};
