import { Link } from 'react-router-dom'

export function UnauthorizedPage() { return <div className="mx-auto max-w-xl py-20 text-center"><h1 className="text-4xl font-black">Access denied</h1><p className="mt-3 text-slate-500">This area is reserved for administrator accounts.</p><Link className="mt-5 inline-block font-bold text-orange-600" to="/">Return to menu</Link></div> }
