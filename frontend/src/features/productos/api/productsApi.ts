import { api } from '@/shared/api'
import type { Product, ProductInput, ProductPage } from '../types/product'

type ProductFilters = { search?: string; categoria_id?: string; disponible?: boolean; skip?: number; limit?: number }

export async function getProducts(params: ProductFilters) { return (await api.get<ProductPage>('/productos', { params })).data }
export function saveProduct(value: ProductInput, id?: number) { return id ? api.put(`/productos/${id}`, value) : api.post('/productos', value) }
export function deactivateProduct(id: number) { return api.delete(`/productos/${id}`) }
export function updateProductStock(id: number, stock: number) { return api.patch(`/productos/${id}/stock`, { stock }) }
