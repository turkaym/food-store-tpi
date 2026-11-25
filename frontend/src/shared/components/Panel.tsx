import type { ReactNode } from 'react'

export function Panel({ children }: { children: ReactNode }) { return <div className="rounded-3xl bg-white p-5 shadow-sm">{children}</div> }
