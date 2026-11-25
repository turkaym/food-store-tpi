import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { getUsers, toggleUser } from '../api/usersApi'

export function useAdminUsers() {
  const client = useQueryClient()
  const users = useQuery({ queryKey: ['admin', 'users'], queryFn: getUsers })
  const toggle = useMutation({ mutationFn: ({ id, disabled }: { id: number; disabled: boolean }) => toggleUser(id, disabled), onSuccess: () => client.invalidateQueries({ queryKey: ['admin', 'users'] }) })
  return { users, toggle }
}
