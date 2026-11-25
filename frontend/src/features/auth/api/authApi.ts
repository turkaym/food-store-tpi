import { api } from '@/shared/api'
import type { User } from '@/features/usuarios'
import type { LoginCredentials, RegisterData } from '../types/auth'

export async function login(credentials: LoginCredentials) { const body = new URLSearchParams(credentials); await api.post('/api/v1/auth/token', body, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }); return getSession() }
export async function register(data: RegisterData) { await api.post('/api/v1/auth/register', data) }
export async function logout() { await api.post('/api/v1/auth/logout') }
export async function getSession() { return (await api.get<User>('/api/v1/auth/me')).data }
