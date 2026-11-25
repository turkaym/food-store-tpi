import { Navigate, Outlet } from 'react-router-dom'
import type { ReactNode } from 'react'
import { Loading } from '@/shared/ui'
import { useAuthStore } from '@/store/authStore'

export function ProtectedRoute({ children, allowedRoles }: { children?: ReactNode; allowedRoles?: string[] }) { const { user, checking } = useAuthStore(); if (checking) return <Loading />; if (!user) return <Navigate to="/login" replace />; if (allowedRoles && !allowedRoles.includes(user.role)) return <Navigate to="/unauthorized" replace />; return children ? <>{children}</> : <Outlet /> }
