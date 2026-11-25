import { Navigate, Route, Routes } from 'react-router-dom'
import { LoginPage, RegisterPage, useAuthSession } from '@/features/auth'
import { AdminCategoriesPage } from '@/features/categorias'
import { AdminOrdersPage, AdminSummaryPage, CartPage, CheckoutPage, OrderDetailPage, OrdersPage } from '@/features/pedidos'
import { AdminProductsPage, CatalogPage } from '@/features/productos'
import { AdminUsersPage } from '@/features/usuarios'
import { AdminLayout, AppLayout } from '@/shared/layout'
import { ProtectedRoute } from './ProtectedRoute'
import { UnauthorizedPage } from './UnauthorizedPage'

export function AppRouter() { useAuthSession(); return <Routes><Route element={<AppLayout />}><Route path="/login" element={<LoginPage />} /><Route path="/register" element={<RegisterPage />} /><Route path="/unauthorized" element={<UnauthorizedPage />} /><Route path="/" element={<CatalogPage />} /><Route path="/carrito" element={<CartPage />} /><Route element={<ProtectedRoute />}><Route path="/checkout" element={<CheckoutPage />} /><Route path="/mis-pedidos" element={<OrdersPage />} /><Route path="/mis-pedidos/:id" element={<OrderDetailPage />} /></Route><Route element={<ProtectedRoute allowedRoles={['admin']} />}><Route path="/admin" element={<Navigate to="/admin/resumen" replace />} /><Route path="/admin" element={<AdminLayout />}><Route path="resumen" element={<AdminSummaryPage />} /><Route path="categorias" element={<AdminCategoriesPage />} /><Route path="productos" element={<AdminProductsPage />} /><Route path="pedidos" element={<AdminOrdersPage />} /><Route path="usuarios" element={<AdminUsersPage />} /></Route></Route><Route path="*" element={<Navigate to="/" replace />} /></Route></Routes> }
