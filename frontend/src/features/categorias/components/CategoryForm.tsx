import { useState } from 'react'
import { useForm } from '@tanstack/react-form'
import { apiError } from '@/shared/api'
import { FieldError } from '@/shared/ui'
import { useSaveCategory } from '../hooks/useCategories'
import type { Category } from '../types/category'

const control = 'mt-1 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 outline-none focus:border-orange-500 focus:ring-2 focus:ring-orange-100'
const button = 'rounded-xl bg-orange-600 px-4 py-2 font-bold text-white disabled:opacity-50'

export function CategoryForm({ category, onDone }: { category?: Category; onDone: () => void }) { const [error, setError] = useState(''); const mutation = useSaveCategory(category?.id, onDone); const form = useForm({ defaultValues: { nombre: category?.nombre ?? '', descripcion: category?.descripcion ?? '' }, onSubmit: async ({ value }) => { try { setError(''); await mutation.mutateAsync(value) } catch (reason) { setError(apiError(reason)) } } }); return <form className="space-y-3" onSubmit={(event) => { event.preventDefault(); void form.handleSubmit() }}><form.Field name="nombre" validators={{ onChange: ({ value }) => value.trim().length < 2 ? 'Use at least 2 characters.' : undefined }}>{(field) => <label className="block text-sm font-semibold">Name<input className={control} value={field.state.value} onBlur={field.handleBlur} onChange={(event) => field.handleChange(event.target.value)} /> <FieldError errors={field.state.meta.errors} /></label>}</form.Field><form.Field name="descripcion">{(field) => <label className="block text-sm font-semibold">Description<textarea className={control} rows={2} value={field.state.value} onChange={(event) => field.handleChange(event.target.value)} /></label>}</form.Field><p className="text-sm text-red-600">{error}</p><button className={button} disabled={mutation.isPending}>{mutation.isPending ? 'Saving...' : category ? 'Save changes' : 'Create category'}</button></form> }
