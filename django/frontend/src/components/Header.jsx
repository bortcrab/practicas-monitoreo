import { Link } from 'react-router-dom'

export default function Header() {
  return (
    <div className="py-4 mb-2">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-4xl font-bold text-blue-950">Productos App</Link>
        <div>
          <Link to="/nuevo-producto" className="bg-green-600 text-white px-4 py-2 rounded-lg">Nuevo Producto</Link>
        </div>
      </div>
    </div>
  )
}
