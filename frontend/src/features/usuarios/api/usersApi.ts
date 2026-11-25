import { api } from '@/shared/api'
import type { User } from '../types/user'

export async function getUsers() { return (await api.get<User[]>('/admin/usuarios')).data }
export function toggleUser(id: number, disabled: boolean) { return api.post(`/admin/usuarios/${id}/${disabled ? 'activar' : 'desactivar'}`) }
