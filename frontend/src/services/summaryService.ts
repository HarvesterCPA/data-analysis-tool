import { api } from './api';
import { ProfitLossSummary, CostBreakdown, RevenueBreakdown, EquipmentAnalysis } from '../types';

export const summaryService = {
  async getProfitLossSummary(harvestSeasonId: number): Promise<ProfitLossSummary> {
    const response = await api.get(`/api/summary/harvest-season/${harvestSeasonId}/profit-loss`);
    return response.data;
  },

  async getCostBreakdown(harvestSeasonId: number): Promise<CostBreakdown> {
    const response = await api.get(`/api/summary/harvest-season/${harvestSeasonId}/cost-breakdown`);
    return response.data;
  },

  async getRevenueBreakdown(harvestSeasonId: number): Promise<RevenueBreakdown> {
    const response = await api.get(`/api/summary/harvest-season/${harvestSeasonId}/revenue-breakdown`);
    return response.data;
  },

  async getEquipmentAnalysis(harvestSeasonId: number): Promise<EquipmentAnalysis> {
    const response = await api.get(`/api/summary/harvest-season/${harvestSeasonId}/equipment-analysis`);
    return response.data;
  },

  async recalculateSummary(harvestSeasonId: number): Promise<void> {
    await api.post(`/api/summary/harvest-season/${harvestSeasonId}/recalculate`);
  },
};
