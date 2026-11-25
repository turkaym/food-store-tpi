export function Loading() { return <div className="grid min-h-40 place-items-center text-slate-500">Loading...</div> }
export function ErrorState({ message }: { message: string }) { return <div role="alert" className="rounded-2xl border border-red-200 bg-red-50 p-5 text-red-800">{message}</div> }
export function EmptyState({ title, message }: { title: string; message: string }) { return <div className="rounded-3xl bg-white p-10 text-center shadow-sm"><h2 className="text-xl font-bold">{title}</h2><p className="mt-2 text-slate-500">{message}</p></div> }
