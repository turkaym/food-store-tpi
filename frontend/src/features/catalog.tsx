import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import { EmptyState, ErrorState } from '@/components'
import { api, apiError } from '@/shared/api'
import { useCartStore } from '@/store/cartStore'
import type { Category, Page, Product } from '@/types'

const pageSize = 9

function CatalogSkeleton() {
  return <div aria-label="Loading products" className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">{Array.from({ length: 6 }, (_, index) => <div className="animate-pulse overflow-hidden rounded-3xl bg-white shadow-sm" key={index}><div className="h-40 bg-orange-100" /><div className="space-y-3 p-5"><div className="h-3 w-24 rounded bg-slate-200" /><div className="h-6 w-2/3 rounded bg-slate-200" /><div className="h-10 rounded bg-slate-100" /><div className="h-10 rounded bg-slate-200" /></div></div>)}</div>
}

export function CatalogPage() {
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [available, setAvailable] = useState(true)
  const [page, setPage] = useState(0)
  const add = useCartStore((state) => state.add)
  const categories = useQuery({ queryKey: ['categories'], queryFn: async () => (await api.get<Category[]>('/api/v1/categorias')).data })
  const skip = page * pageSize
  const products = useQuery({
    queryKey: ['products', { search, category, available, skip, limit: pageSize }],
    queryFn: async () => (await api.get<Page<Product>>('/api/v1/productos', { params: { search: search || undefined, categoria_id: category || undefined, disponible: available, skip, limit: pageSize } })).data,
    placeholderData: keepPreviousData,
  })
  const pageCount = Math.ceil((products.data?.total ?? 0) / pageSize)
  const changeFilter = (update: () => void) => { update(); setPage(0) }
  const resetFilters = () => { setSearch(''); setCategory(''); setAvailable(true); setPage(0) }

  return <div><div className="mb-8 max-w-2xl"><p className="font-bold uppercase tracking-[0.2em] text-orange-600">Fresh, simple, yours</p><h1 className="mt-2 text-4xl font-black tracking-tight sm:text-5xl">Good food for busy days.</h1><p className="mt-3 text-slate-500">Browse today&apos;s menu and build your order in a few clicks.</p></div><div className="mb-8 grid gap-3 rounded-2xl bg-white p-4 shadow-sm sm:grid-cols-[1fr_200px_auto_auto]"><label className="sr-only" htmlFor="search">Search products</label><input id="search" className="rounded-xl border px-3 py-2" placeholder="Search the menu" value={search} onChange={(event) => changeFilter(() => setSearch(event.target.value))} /><select aria-label="Category" className="rounded-xl border px-3 py-2" value={category} onChange={(event) => changeFilter(() => setCategory(event.target.value))}><option value="">All categories</option>{categories.data?.map((item) => <option key={item.id} value={item.id}>{item.nombre}</option>)}</select><label className="flex items-center gap-2 px-2 text-sm"><input type="checkbox" checked={available} onChange={(event) => changeFilter(() => setAvailable(event.target.checked))} /> In stock only</label><button className="rounded-xl border px-3 py-2 text-sm font-bold text-slate-600" type="button" onClick={resetFilters}>Clear filters</button></div>{categories.isError ? <ErrorState message={apiError(categories.error)} /> : products.isLoading ? <CatalogSkeleton /> : products.isError ? <ErrorState message={apiError(products.error)} /> : products.data?.items.length === 0 ? <EmptyState title="No matches" message="Try another search or category." /> : <><div className={`grid gap-5 sm:grid-cols-2 lg:grid-cols-3 ${products.isFetching ? 'opacity-60' : ''}`}>{products.data?.items.map((product) => <article key={product.id} className="overflow-hidden rounded-3xl bg-white shadow-sm"><div className="flex h-40 items-center justify-center bg-orange-50 text-sm font-black uppercase tracking-[0.25em] text-orange-600">{product.imagen_url ? <img className="h-full w-full object-cover" src={product.imagen_url} alt="" /> : 'Mesa24'}</div><div className="p-5"><p className="text-xs font-bold uppercase tracking-wider text-orange-600">{product.categoria.nombre}</p><h2 className="mt-1 text-xl font-bold">{product.nombre}</h2><p className="mt-2 min-h-10 text-sm text-slate-500">{product.descripcion}</p><div className="mt-5 flex items-center justify-between"><span className="text-xl font-black">${Number(product.precio_base).toFixed(2)}</span><button disabled={!product.disponible || product.stock < 1} onClick={() => add(product)} className="rounded-xl bg-slate-900 px-4 py-2 text-sm font-bold text-white disabled:cursor-not-allowed disabled:bg-slate-300">{product.stock < 1 ? 'Out of stock' : 'Add'}</button></div></div></article>)}</div><nav aria-label="Catalog pagination" className="mt-8 flex items-center justify-center gap-4"><button className="rounded-xl border bg-white px-4 py-2 font-bold disabled:opacity-40" disabled={page === 0 || products.isFetching} onClick={() => setPage((current) => current - 1)}>Previous</button><span className="text-sm font-semibold text-slate-600">Page {page + 1} of {pageCount}</span><button className="rounded-xl border bg-white px-4 py-2 font-bold disabled:opacity-40" disabled={page + 1 >= pageCount || products.isFetching} onClick={() => setPage((current) => current + 1)}>Next</button></nav></>}</div>
}
