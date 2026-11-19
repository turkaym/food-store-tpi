import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { Product } from '@/types'
export type CartLine = { product: Product; quantity: number }
type CartState = { lines: CartLine[]; add: (product: Product) => void; update: (id: number, quantity: number) => void; remove: (id: number) => void; clear: () => void }
export const useCartStore = create<CartState>()(persist((set) => ({
  lines: [],
  add: (product) => set((state) => { const existing = state.lines.find((line) => line.product.id === product.id); return { lines: existing ? state.lines.map((line) => line.product.id === product.id ? { ...line, quantity: Math.min(line.quantity + 1, product.stock) } : line) : [...state.lines, { product, quantity: 1 }] } }),
  update: (id, quantity) => set((state) => ({ lines: quantity < 1 ? state.lines.filter((line) => line.product.id !== id) : state.lines.map((line) => line.product.id === id ? { ...line, quantity: Math.min(quantity, line.product.stock) } : line) })),
  remove: (id) => set((state) => ({ lines: state.lines.filter((line) => line.product.id !== id) })), clear: () => set({ lines: [] }),
}), { name: 'food-store-cart' }))
