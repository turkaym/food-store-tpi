import { api } from '@/shared/api'
import type { Product, ProductInput, ProductPage } from '../types/product'

type ProductFilters = { search?: string; categoria_id?: string; disponible?: boolean; skip?: number; limit?: number }

export async function getProducts(params: ProductFilters) { return (await api.get<ProductPage>('/api/v1/productos', { params })).data }
export function saveProduct(value: ProductInput, id?: number) { return id ? api.put(`/api/v1/productos/${id}`, value) : api.post('/api/v1/productos', value) }
export function deactivateProduct(id: number) { return api.delete(`/api/v1/productos/${id}`) }
export function updateProductStock(id: number, stock: number) { return api.patch(`/api/v1/productos/${id}/stock`, { stock }) }
