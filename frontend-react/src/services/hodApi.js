import { apiClient } from './api';

export const hodApi = {
  dashboard: (departmentId) => apiClient.get('/hod/dashboard', { params: departmentId ? { department_id: departmentId } : {} }),
  department: (departmentId) => apiClient.get('/hod/department', { params: departmentId ? { department_id: departmentId } : {} }),
  faculty: (params) => apiClient.get('/hod/faculty', { params }),
  students: (params) => apiClient.get('/hod/students', { params }),
  academicStructure: (departmentId) => apiClient.get('/hod/academic-structure', { params: departmentId ? { department_id: departmentId } : {} }),
  assignments: (departmentId) => apiClient.get('/hod/faculty-assignments', { params: departmentId ? { department_id: departmentId } : {} }),
  announcements: (departmentId) => apiClient.get('/hod/announcements', { params: departmentId ? { department_id: departmentId } : {} }),
  createAnnouncement: (payload) => apiClient.post('/hod/announcements', payload),
  updateAnnouncement: (id, payload) => apiClient.put(`/hod/announcements/${id}`, payload),
  reports: (departmentId) => apiClient.get('/hod/reports', { params: departmentId ? { department_id: departmentId } : {} }),
};
