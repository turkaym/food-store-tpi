import type { Category } from '@/features/categorias'

export type Product = { id: number; categoria_id: number; nombre: string; descripcion: string; precio_base: number; imagen_url: string; stock: number; disponible: boolean; activo: boolean; categoria: Category }
export type ProductInput = { categoria_id: number; nombre: string; descripcion: string; precio_base: number; imagen_url: string; stock: number; disponible: boolean }
export type ProductPage = { total: number; items: Product[] }
