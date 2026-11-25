import { useEffect } from 'react'
import { useAuthStore } from '@/store/authStore'

export function useAuthSession() { const checkSession = useAuthStore((state) => state.checkSession); useEffect(() => { void checkSession() }, [checkSession]) }
