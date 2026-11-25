import { api } from '@/shared/api'
import type { CreateOrderInput, Order, OrderPage, OrderSummary } from '../types/order'

export async function getOrders(admin = false) { return (await api.get<OrderPage>('/api/v1/pedidos', admin ? { params: { limit: 100 } } : undefined)).data }
export async function getOrder(id: string) { return (await api.get<Order>(`/api/v1/pedidos/${id}`)).data }
export async function getOrderSummary() { return (await api.get<OrderSummary>('/api/v1/pedidos/resumen')).data }
export function createOrder(value: CreateOrderInput) { return api.post<Order>('/api/v1/pedidos', value) }
export function cancelOrder(id: string | number) { return api.patch(`/api/v1/pedidos/${id}/cancelar`) }
export function updateOrderStatus(id: number, estado: string) { return api.patch(`/api/v1/pedidos/${id}/estado`, { estado }) }
