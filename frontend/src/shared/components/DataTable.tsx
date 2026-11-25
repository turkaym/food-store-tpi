import { flexRender } from '@tanstack/react-table'
import type { Header, Table as TanStackTable } from '@tanstack/react-table'
import type { ReactNode } from 'react'

export function Table({ children }: { children: ReactNode }) { return <div className="overflow-x-auto rounded-3xl bg-white shadow-sm"><table className="w-full min-w-[680px] text-left">{children}</table></div> }
export function TableHead<T>({ headers }: { headers: Header<T, unknown>[] }) { return <thead className="border-b bg-slate-50 text-sm text-slate-500"><tr>{headers.map((header) => <th className="px-5 py-4 font-semibold" key={header.id}>{flexRender(header.column.columnDef.header, header.getContext())}</th>)}</tr></thead> }
export function TablePagination<T>({ table }: { table: TanStackTable<T> }) { return <div className="mt-4 flex items-center justify-end gap-3 text-sm"><button className="rounded-lg border bg-white px-3 py-2 font-bold disabled:opacity-40" disabled={!table.getCanPreviousPage()} onClick={() => table.previousPage()}>Previous</button><span className="font-semibold text-slate-600">Page {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}</span><button className="rounded-lg border bg-white px-3 py-2 font-bold disabled:opacity-40" disabled={!table.getCanNextPage()} onClick={() => table.nextPage()}>Next</button></div> }
