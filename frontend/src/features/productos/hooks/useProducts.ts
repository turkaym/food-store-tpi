import { keepPreviousData, useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { deactivateProduct, getProducts, saveProduct, updateProductStock } from '../api/productsApi'
import type { ProductInput } from '../types/product'

export function useCatalogProducts(filters: { search: string; category: string; available: boolean; skip: number; limit: number }) { return useQuery({ queryKey: ['products', filters], queryFn: () => getProducts({ search: filters.search || undefined, categoria_id: filters.category || undefined, disponible: filters.available, skip: filters.skip, limit: filters.limit }), placeholderData: keepPreviousData }) }
export function useAdminProducts(search: string, category: string) { return useQuery({ queryKey: ['products', search, category], queryFn: () => getProducts({ search: search || undefined, categoria_id: category || undefined, limit: 100 }) }) }
export function useSaveProduct(id: number | undefined, onDone: () => void) { const client = useQueryClient(); return useMutation({ mutationFn: (value: ProductInput) => saveProduct(value, id), onSuccess: async () => { await client.invalidateQueries({ queryKey: ['products'] }); onDone() } }) }
export function useDeactivateProduct() { const client = useQueryClient(); return useMutation({ mutationFn: deactivateProduct, onSuccess: () => client.invalidateQueries({ queryKey: ['products'] }) }) }
export function useUpdateProductStock() { const client = useQueryClient(); return useMutation({ mutationFn: ({ id, value }: { id: number; value: number }) => updateProductStock(id, value), onSuccess: () => client.invalidateQueries({ queryKey: ['products'] }) }) }
