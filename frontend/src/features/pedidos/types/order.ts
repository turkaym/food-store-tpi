export type OrderItem = { producto_id: number; nombre_producto: string; precio_unitario: number; cantidad: number; subtotal: number }
export type Order = { id: number; usuario_id: number; estado: string; forma_pago: string; direccion_entrega: string; notas: string | null; total: number; created_at: string; updated_at: string; items: OrderItem[] }
export type OrderPage = { total: number; items: Order[] }
export type OrderSummary = { pendientes: number; en_preparacion: number; entregados: number; cancelados: number; pedidos_hoy: number; ingresos_entregados: number }
export type CheckoutInput = { forma_pago: 'EFECTIVO' | 'TRANSFERENCIA'; direccion_entrega: string; notas: string }
export type CreateOrderInput = CheckoutInput & { items: { producto_id: number; cantidad: number }[] }
