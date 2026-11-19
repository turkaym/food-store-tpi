export type User = { id: number; username: string; full_name: string; email: string; role: string; disabled: boolean; created_at?: string }
export type Category = { id: number; nombre: string; descripcion: string; activo: boolean }
export type Product = { id: number; categoria_id: number; nombre: string; descripcion: string; precio_base: number; imagen_url: string; stock: number; disponible: boolean; activo: boolean; categoria: Category }
export type OrderItem = { producto_id: number; nombre_producto: string; precio_unitario: number; cantidad: number; subtotal: number }
export type Order = { id: number; usuario_id: number; estado: string; forma_pago: string; direccion_entrega: string; notas: string | null; total: number; created_at: string; updated_at: string; items: OrderItem[] }
export type Page<T> = { total: number; items: T[] }
export type OrderSummary = { pendientes: number; en_preparacion: number; entregados: number; cancelados: number; pedidos_hoy: number; ingresos_entregados: number }
