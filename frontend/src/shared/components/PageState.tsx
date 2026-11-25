import type { ReactNode } from 'react'
import { apiError } from '@/shared/api'
import { ErrorState, Loading } from '@/shared/ui'

export function PageState({ query, children }: { query: { isLoading: boolean; isError: boolean; error: unknown }; children: ReactNode }) { if (query.isLoading) return <Loading />; if (query.isError) return <ErrorState message={apiError(query.error)} />; return <>{children}</> }
