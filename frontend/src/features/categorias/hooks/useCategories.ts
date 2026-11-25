import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { deactivateCategory, getCategories, saveCategory } from '../api/categoriesApi'
import type { CategoryInput } from '../types/category'

export function useCategories() { return useQuery({ queryKey: ['categories'], queryFn: getCategories }) }
export function useSaveCategory(id: number | undefined, onDone: () => void) { const client = useQueryClient(); return useMutation({ mutationFn: (value: CategoryInput) => saveCategory(value, id), onSuccess: async () => { await client.invalidateQueries({ queryKey: ['categories'] }); onDone() } }) }
export function useDeactivateCategory() { const client = useQueryClient(); return useMutation({ mutationFn: deactivateCategory, onSuccess: () => client.invalidateQueries({ queryKey: ['categories'] }) }) }
