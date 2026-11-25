import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { registerSessionFailureHandler } from '@/shared/api'
import { getSession, login as loginRequest, logout as logoutRequest, register as registerRequest } from '@/features/auth/api'
import type { RegisterData } from '@/features/auth/types'
import type { User } from '@/features/usuarios'

type AuthState = { user: User | null; checking: boolean; loading: boolean; login: (username: string, password: string) => Promise<void>; register: (data: RegisterData) => Promise<void>; logout: () => Promise<void>; checkSession: () => Promise<void> }
export const useAuthStore = create<AuthState>()(persist((set) => ({
  user: null, checking: true, loading: false,
  login: async (username, password) => { set({ loading: true }); try { set({ user: await loginRequest({ username, password }) }) } finally { set({ loading: false }) } },
  register: async (data) => { set({ loading: true }); try { await registerRequest(data) } finally { set({ loading: false }) } },
  logout: async () => { try { await logoutRequest() } finally { set({ user: null }) } },
  checkSession: async () => { try { set({ user: await getSession() }) } catch { set({ user: null }) } finally { set({ checking: false }) } },
}), {
  name: 'food-store-auth',
  partialize: (state) => ({ user: state.user }),
}))

registerSessionFailureHandler(() => useAuthStore.setState({ user: null }))
