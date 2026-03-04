import axios from 'axios'

const productsApi = axios.create({
    baseURL: '/api/producto'
})

export const getProducts = () => productsApi.get()
export const getProduct = (id) => productsApi.get(`${id}`)
export const createProduct = (product) => productsApi.post('/', product)
export const updateProduct = (id, product) => productsApi.put(`/${id}/`, product)
export const deleteProduct = (id) => productsApi.delete(`/${id}/`)
