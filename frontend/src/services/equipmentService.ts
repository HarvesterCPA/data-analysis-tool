import { api } from './api';
import { Equipment } from '../types';

export const equipmentService = {
  async getEquipmentByHarvestSeason(harvestSeasonId: number): Promise<Equipment[]> {
    const response = await api.get(`/api/equipment/harvest-season/${harvestSeasonId}`);
    return response.data;
  },

  async getEquipment(id: number): Promise<Equipment> {
    const response = await api.get(`/api/equipment/${id}`);
    return response.data;
  },

  async createEquipment(data: Partial<Equipment>): Promise<Equipment> {
    const response = await api.post('/api/equipment/', data);
    return response.data;
  },

  async updateEquipment(id: number, data: Partial<Equipment>): Promise<Equipment> {
    const response = await api.put(`/api/equipment/${id}`, data);
    return response.data;
  },

  async deleteEquipment(id: number): Promise<void> {
    await api.delete(`/api/equipment/${id}`);
  },

  async calculateEquipmentCosts(id: number): Promise<void> {
    await api.post(`/api/equipment/${id}/calculate-costs`);
  },
};
