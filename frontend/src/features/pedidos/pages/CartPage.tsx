import { Link } from 'react-router-dom'
import { EmptyState } from '@/shared/ui'
import { useCartStore } from '@/store/cartStore'
import { CartLines } from '../components/CartLines'

export function CartPage() { const lines = useCartStore((state) => state.lines); const total = lines.reduce((sum, line) => sum + Number(line.product.precio_base) * line.quantity, 0); if (!lines.length) return <EmptyState title="Your cart is empty" message="Add something delicious from the menu to get started." />; return <section><div className="flex items-end justify-between"><div><p className="font-bold uppercase tracking-[0.2em] text-orange-600">Your selection</p><h1 className="mt-2 text-4xl font-black">Cart</h1></div><Link className="text-sm font-bold text-orange-600" to="/">Continue shopping</Link></div><div className="mt-8 grid gap-8 lg:grid-cols-[1fr_320px]"><CartLines /><aside className="h-fit rounded-3xl bg-slate-900 p-6 text-white"><p className="text-sm text-slate-300">Order total</p><p className="mt-2 text-3xl font-black">${total.toFixed(2)}</p><Link to="/checkout" className="mt-6 block rounded-xl bg-orange-500 px-4 py-3 text-center font-bold">Checkout</Link></aside></div></section> }
