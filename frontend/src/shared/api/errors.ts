import axios from 'axios'

export function apiError(error: unknown) {
  return axios.isAxiosError(error) ? (error.response?.data?.detail ?? 'The request could not be completed.') : 'The request could not be completed.'
}
