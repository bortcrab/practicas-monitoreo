import { Head, useForm } from '@inertiajs/react';
import AppLayout from '@/layouts/app-layout';
import type { BreadcrumbItem } from '@/types';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { store } from '@/actions/App/Http/Controllers/ProductController';

const breadcrumbs: BreadcrumbItem[] = [
    {
        title: 'Create',
        href: '/products/create',
    },
];

export default function Create() {
    const {data, setData, post, processing, errors} = useForm({
        name: '',
        description: '',
        stock: '',
        price: '',
    })

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        post(store());
    }

    return (
        <AppLayout breadcrumbs={breadcrumbs}>
            <Head title="Products | Create" />
            <div className='w-8/12 p-4'>
                <form onSubmit={handleSubmit} method='post' className='space-y-4'>
                    <div className='gap-1.5'>
                        <Input
                            placeholder='Product Name'
                            value={data.name}
                            onChange={e => setData('name', e.target.value)}
                        />
                        {errors.name && (
                            <div className='flex items-center text-red-500 text-sm mt-1'>
                                {errors.name}
                            </div>
                        )}
                    </div>
                    <div className='gap-1.5'>
                        <Input
                            type='number'
                            placeholder='Product Stock'
                            value={data.stock}
                            onChange={e => setData('stock', e.target.value)}
                        />
                        {errors.stock && (
                            <div className='flex items-center text-red-500 text-sm mt-1'>
                                {errors.stock}
                            </div>
                        )}
                    </div>
                    <div className='gap-1.5'>
                        <Input
                            type='number'
                            placeholder='Product Price'
                            value={data.price}
                            onChange={e => setData('price', e.target.value)}
                        />
                        {errors.price && (
                            <div className='flex items-center text-red-500 text-sm mt-1'>
                                {errors.price}
                            </div>
                        )}
                    </div>
                    <div className='gap-1.5'>
                        <Textarea
                            placeholder='Product Description'
                            value={data.description}
                            onChange={e => setData('description', e.target.value)}
                        />
                        {errors.description && (
                            <div className='flex items-center text-red-500 text-sm mt-1'>
                                {errors.description}
                            </div>
                        )}
                    </div>
                    <Button type='submit'>Create product</Button>
                </form>
            </div>
        </AppLayout>
    );
}
