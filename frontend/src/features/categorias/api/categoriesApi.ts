import { api } from '@/shared/api'
import type { Category, CategoryInput } from '../types/category'

export async function getCategories() { return (await api.get<Category[]>('/api/v1/categorias')).data }
export function saveCategory(value: CategoryInput, id?: number) { return id ? api.put(`/api/v1/categorias/${id}`, value) : api.post('/api/v1/categorias', value) }
export function deactivateCategory(id: number) { return api.delete(`/api/v1/categorias/${id}`) }
