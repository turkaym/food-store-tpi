import { useEffect } from 'react'
import { Link, Navigate, Route, Routes } from 'react-router-dom'
import { Layout, ProtectedRoute } from '@/components'
import { useAuthStore } from '@/store/authStore'
import { LoginPage, RegisterPage } from '@/features/auth'
import { CatalogPage } from '@/features/catalog'
import { CartPage, CheckoutPage } from '@/features/cart'
import { OrdersPage, OrderDetailPage } from '@/features/orders'
import { AdminCategoriesPage, AdminLayout, AdminOrdersPage, AdminProductsPage, AdminSummaryPage, AdminUsersPage } from '@/features/admin'

export default function App() { const checkSession = useAuthStore((s) => s.checkSession); useEffect(() => { void checkSession() }, [checkSession]); return <Routes><Route element={<Layout />}><Route path="/login" element={<LoginPage />} /><Route path="/register" element={<RegisterPage />} /><Route path="/unauthorized" element={<div className="mx-auto max-w-xl py-20 text-center"><h1 className="text-4xl font-black">Access denied</h1><p className="mt-3 text-slate-500">This area is reserved for administrator accounts.</p><Link className="mt-5 inline-block font-bold text-orange-600" to="/">Return to menu</Link></div>} /><Route path="/" element={<CatalogPage />} /><Route path="/carrito" element={<CartPage />} /><Route element={<ProtectedRoute />}><Route path="/checkout" element={<CheckoutPage />} /><Route path="/mis-pedidos" element={<OrdersPage />} /><Route path="/mis-pedidos/:id" element={<OrderDetailPage />} /></Route><Route element={<ProtectedRoute allowedRoles={['admin']} />}><Route path="/admin" element={<Navigate to="/admin/resumen" replace />} /><Route path="/admin" element={<AdminLayout />}><Route path="resumen" element={<AdminSummaryPage />} /><Route path="categorias" element={<AdminCategoriesPage />} /><Route path="productos" element={<AdminProductsPage />} /><Route path="pedidos" element={<AdminOrdersPage />} /><Route path="usuarios" element={<AdminUsersPage />} /></Route></Route><Route path="*" element={<Navigate to="/" replace />} /></Route></Routes> }
