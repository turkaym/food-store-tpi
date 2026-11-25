import { api } from '@/shared/api'
import type { Category, CategoryInput } from '../types/category'

export async function getCategories() { return (await api.get<Category[]>('/categorias')).data }
export function saveCategory(value: CategoryInput, id?: number) { return id ? api.put(`/categorias/${id}`, value) : api.post('/categorias', value) }
export function deactivateCategory(id: number) { return api.delete(`/categorias/${id}`) }
