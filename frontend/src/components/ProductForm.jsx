import { useState, useEffect } from "react"
import { useNavigate } from "react-router"
import { useParams } from "react-router-dom"
import { createProduct, getProduct, updateProduct } from "../api/products"
import toast from "react-hot-toast"

export default function ProductForm() {

  const [product, setProduct] = useState({
    nombre: '',
    precio: 0,
    descripcion: '',
  })

  const navigate = useNavigate()
  const params = useParams()

  useEffect(() => {
    const loadProduct = async () => {
      if (params.id) {
        const response = await getProduct(params.id)
        setProduct(response.data)
      }
    }
    loadProduct()
  }, [params.id])

  const handleCancel = () => {
    navigate('/')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (params.id) {
      await updateProduct(params.id, product)
      toast.success('Producto editado correctamente')
    } else {
      await createProduct(product)
      toast.success('Producto creado correctamente')
    }
    navigate('/')
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-bold text-gray-700">Nombre</label>
          <input value={product.nombre} onChange={(e) => setProduct({...product, nombre: e.target.value})} type="text" required className="w-full mt-1 p-2 border border-gray-300 rounded"/>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-bold text-gray-700">Precio</label>
          <input value={product.precio} onChange={(e) => setProduct({...product, precio: e.target.value})} type="number" required className="w-full mt-1 p-2 border border-gray-300 rounded"/>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-bold text-gray-700">Descripción</label>
          <textarea value={product.descripcion} onChange={(e) => setProduct({...product, descripcion: e.target.value})} required className="w-full mt-1 p-2 border border-gray-300 rounded">
          </textarea>
        </div>

        <div className="mt-4">
          <button className="bg-green-600 text-white px-4 py-2 rounded-lg">Guardar</button>
          <button type="button" onClick={handleCancel} className="bg-red-600 text-white px-4 py-2 rounded-lg ml-2">Cancelar</button>
        </div>
      </form>
    </div>
  )
}
