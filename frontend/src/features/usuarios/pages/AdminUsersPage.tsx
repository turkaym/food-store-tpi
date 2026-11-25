import { useAuthStore } from '@/store/authStore'
import { PageState } from '@/shared/components'
import { EmptyState } from '@/shared/ui'
import { UsersTable } from '../components/UsersTable'
import { useAdminUsers } from '../hooks/useAdminUsers'

export function AdminUsersPage() { const currentUser = useAuthStore((state) => state.user); const { users, toggle } = useAdminUsers(); return <PageState query={users}>{!users.data?.length ? <EmptyState title="No users" message="There are no registered accounts." /> : <UsersTable users={users.data} currentUserId={currentUser?.id} onToggle={(user) => void toggle.mutateAsync({ id: user.id, disabled: user.disabled })} />}</PageState> }
