import axios from 'axios'
import { clearClientSession } from '@/shared/session'

export const api = axios.create({ baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000', withCredentials: true, headers: { 'Content-Type': 'application/json' } })

api.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status
      const detail = error.response?.data?.detail
      const requestPath = error.config?.url ?? ''
      const isAuthRequest = requestPath.includes('/auth/token') || requestPath.includes('/auth/me')
      const sessionExpired = status === 401 && !isAuthRequest
      const accountDisabled = status === 400 && detail === 'Cuenta de usuario desactivada'

      if (sessionExpired || accountDisabled) {
        clearClientSession()
        if (window.location.pathname !== '/login') window.location.assign('/login')
      }
    }

    return Promise.reject(error)
  },
)

export function apiError(error: unknown) { return axios.isAxiosError(error) ? (error.response?.data?.detail ?? 'The request could not be completed.') : 'The request could not be completed.' }
