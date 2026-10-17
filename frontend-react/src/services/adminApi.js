import { apiClient } from './api';

export const adminApi = {
  dashboard: () => apiClient.get('/admin/dashboard'),
  getProfile: () => apiClient.get('/admin/profile'),
  updateProfile: (payload) => apiClient.put('/admin/profile', payload),
  departments: (params) => apiClient.get('/admin/departments', { params }),
  createDepartment: (payload) => apiClient.post('/admin/departments', payload),
  updateDepartment: (id, payload) => apiClient.patch(`/admin/departments/${id}`, payload),
  academicYears: () => apiClient.get('/admin/academic-years'),
  createAcademicYear: (payload) => apiClient.post('/admin/academic-years', payload),
  announcements: () => apiClient.get('/admin/announcements'),
  createAnnouncement: (payload) => apiClient.post('/admin/announcements', payload),
  updateAnnouncement: (id, payload) => apiClient.patch(`/admin/announcements/${id}`, payload),
  auditLogs: (params) => apiClient.get('/admin/audit-logs', { params }),
};
