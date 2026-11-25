import type { ReactNode } from 'react'

export const authInput = 'mt-1 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 outline-none focus:border-orange-500 focus:ring-2 focus:ring-orange-100'
export function AuthShell({ title, children }: { title: string; children: ReactNode }) { return <section className="mx-auto max-w-md rounded-3xl bg-white p-7 shadow-sm"><p className="text-sm font-bold uppercase tracking-[0.2em] text-orange-600">Mesa24</p><h1 className="mt-2 text-3xl font-black">{title}</h1>{children}</section> }
