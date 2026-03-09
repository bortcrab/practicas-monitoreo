import AppLayout from '@/layouts/app-layout';
import { type BreadcrumbItem, Product } from '@/types';
import { Head, Link, router } from '@inertiajs/react';
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { Button } from '@/components/ui/button';
import { create, edit, destroy } from '@/actions/App/Http/Controllers/ProductController';

const breadcrumbs: BreadcrumbItem[] = [
    {
        title: 'Products',
        href: '/products',
    },
];

export default function Index({ products }: { products: Product[] }) {

    const handleDelete = (product: Product) => {
        if (confirm('Are you sure you want to delete this product?')) {
            router.delete(destroy(product).url);
        }
    }

    return (
        <AppLayout breadcrumbs={breadcrumbs}>
            <Head title="Products | List" />
            <div className="m-4">
                <Link href={create().url}>
                    <Button className="mb-4">
                        Create Product
                    </Button>
                </Link>

                {products.length > 0 && (
                    <Table>
                        <TableCaption>A list of all products.</TableCaption>
                        <TableHeader>
                            <TableRow>
                                <TableHead className="w-[100px]">ID</TableHead>
                                <TableHead>Name</TableHead>
                                <TableHead>Description</TableHead>
                                <TableHead>Stock</TableHead>
                                <TableHead>Price</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {products.map((product) => (
                                <TableRow key={product.id}>
                                    <TableCell className="font-medium">{product.id}</TableCell>
                                    <TableCell>{product.name}</TableCell>
                                    <TableCell>{product.description}</TableCell>
                                    <TableCell>{product.stock}</TableCell>
                                    <TableCell>{product.price}</TableCell>
                                    <TableCell className="text-right space-x-2">
                                        <Link href={edit(product).url}>
                                            <Button className='bg-slate-500'>Edit</Button>
                                        </Link>
                                        <Button
                                            className='bg-red-500'
                                            onClick={() => handleDelete(product)}
                                        >
                                            Delete
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                )}
            </div>
        </AppLayout>
    );
}
