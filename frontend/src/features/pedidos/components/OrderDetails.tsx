import type { Order } from '../types/order'

export const money = (value: number) => `$${Number(value).toFixed(2)}`

export function AdminOrderDetails({ order }: { order: Order }) { return <div className="bg-orange-50 px-5 py-4 text-sm"><p><strong>Customer ID:</strong> {order.usuario_id} · <strong>Payment:</strong> {order.forma_pago} · <strong>Address:</strong> {order.direccion_entrega}</p><div className="mt-3 space-y-1">{order.items.map((item) => <p key={item.producto_id}>{item.nombre_producto} x {item.cantidad} <span className="float-right font-bold">{money(item.subtotal)}</span></p>)}</div>{order.notas && <p className="mt-3"><strong>Notes:</strong> {order.notas}</p>}</div> }
