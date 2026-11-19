import { create } from 'zustand'
import { api } from '@/shared/api'
import type { User } from '@/types'

type AuthState = { user: User | null; checking: boolean; loading: boolean; login: (username: string, password: string) => Promise<void>; register: (data: { username: string; full_name: string; email: string; password: string }) => Promise<void>; logout: () => Promise<void>; checkSession: () => Promise<void> }
export const useAuthStore = create<AuthState>((set) => ({
  user: null, checking: true, loading: false,
  login: async (username, password) => { set({ loading: true }); try { const body = new URLSearchParams({ username, password }); await api.post('/api/v1/auth/token', body, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }); const { data } = await api.get<User>('/api/v1/auth/me'); set({ user: data }) } finally { set({ loading: false }) } },
  register: async (data) => { set({ loading: true }); try { await api.post('/api/v1/auth/register', data) } finally { set({ loading: false }) } },
  logout: async () => { try { await api.post('/api/v1/auth/logout') } finally { set({ user: null }) } },
  checkSession: async () => { try { const { data } = await api.get<User>('/api/v1/auth/me'); set({ user: data }) } catch { set({ user: null }) } finally { set({ checking: false }) } },
}))
