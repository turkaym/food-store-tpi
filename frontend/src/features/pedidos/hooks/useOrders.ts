import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import type { CartLine } from '@/store/cartStore'
import { cancelOrder, createOrder, getOrder, getOrders, getOrderSummary, updateOrderStatus } from '../api/ordersApi'
import type { CheckoutInput } from '../types/order'

export function useOrders() { return useQuery({ queryKey: ['orders'], queryFn: () => getOrders() }) }
export function useOrder(id: string | undefined) { return useQuery({ queryKey: ['order', id], queryFn: () => getOrder(id!), enabled: Boolean(id) }) }
export function useCancelOrder(id: string | undefined, onError?: (reason: unknown) => void) { const client = useQueryClient(); return useMutation({ mutationFn: () => cancelOrder(id!), onSuccess: async () => { await client.invalidateQueries({ queryKey: ['orders'] }); await client.invalidateQueries({ queryKey: ['order', id] }) }, onError }) }
export function useCreateOrder(lines: CartLine[], onSuccess: (id: number) => void, onError: (reason: unknown) => void) { return useMutation({ mutationFn: (value: CheckoutInput) => createOrder({ ...value, items: lines.map((line) => ({ producto_id: line.product.id, cantidad: line.quantity })) }), onSuccess: (response) => onSuccess(response.data.id), onError }) }

export function useAdminOrders() { return useQuery({ queryKey: ['admin', 'orders'], queryFn: () => getOrders(true) }) }
export function useOrderSummary() { return useQuery({ queryKey: ['admin', 'summary'], queryFn: getOrderSummary }) }
export function useUpdateOrderStatus() { const client = useQueryClient(); return useMutation({ mutationFn: ({ id, estado }: { id: number; estado: string }) => updateOrderStatus(id, estado), onSuccess: async () => { await client.invalidateQueries({ queryKey: ['admin', 'orders'] }); await client.invalidateQueries({ queryKey: ['admin', 'summary'] }) } }) }
export function useAdminCancelOrder() { const client = useQueryClient(); return useMutation({ mutationFn: (id: number) => cancelOrder(id), onSuccess: async () => { await client.invalidateQueries({ queryKey: ['admin', 'orders'] }); await client.invalidateQueries({ queryKey: ['admin', 'summary'] }) } }) }
