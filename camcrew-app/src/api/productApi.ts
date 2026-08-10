import { apiClient } from './client';
import { Product, ProductType } from '../types/product';
import { MOCK_PRODUCTS } from './mockData';

const mapProduct = (p: any): Product => ({
  id: String(p.id || 'prod_' + Math.random()),
  name: p.name || 'Equipment item',
  brand: p.brand || 'Sony',
  category: p.category || 'Cameras',
  type: (p.type as ProductType) || (p.rental_price_per_day ? 'rental' : 'sale'),
  price: Number(p.price || 0),
  rentalPricePerDay: p.rental_price_per_day ? Number(p.rental_price_per_day) : (p.rentalPricePerDay || 2500),
  condition: p.condition || 'New',
  image: p.image_url || p.image || 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?q=80&w=800',
  description: p.description || '',
  specs: p.specs || { Resolution: '4K 120p', Sensor: 'Full Frame' },
  inStock: p.in_stock !== undefined ? Boolean(p.in_stock) : true,
  rating: Number(p.rating || 5.0),
});

export const productApi = {
  getProducts: async (type?: ProductType, category?: string, searchQuery?: string): Promise<Product[]> => {
    try {
      const res = await apiClient.get('/products', { params: { type, category, searchQuery } });
      let rawList: any[] = [];
      if (Array.isArray(res.data)) rawList = res.data;
      else if (res.data && Array.isArray(res.data.products)) rawList = res.data.products;
      else if (res.data && Array.isArray(res.data.data)) rawList = res.data.data;

      const dbProducts = rawList.map(mapProduct);
      let combined = [...dbProducts, ...MOCK_PRODUCTS];

      // Remove duplicate IDs
      const map = new Map<string, Product>();
      combined.forEach(p => {
        if (!map.has(p.id)) map.set(p.id, p);
      });
      let list: Product[] = Array.from(map.values());

      if (type) list = list.filter(p => p.type === type);
      if (category && category !== 'All') {
        const catClean = category.toLowerCase();
        list = list.filter(p => p.category.toLowerCase().includes(catClean));
      }
      if (searchQuery) {
        const q = searchQuery.toLowerCase();
        list = list.filter(p => p.name.toLowerCase().includes(q) || p.brand.toLowerCase().includes(q));
      }
      return list;
    } catch (e) {
      let list = [...MOCK_PRODUCTS];
      if (type) list = list.filter(p => p.type === type);
      if (category && category !== 'All') {
        const catClean = category.toLowerCase();
        list = list.filter(p => p.category.toLowerCase().includes(catClean));
      }
      if (searchQuery) {
        const q = searchQuery.toLowerCase();
        list = list.filter(p => p.name.toLowerCase().includes(q) || p.brand.toLowerCase().includes(q));
      }
      return list;
    }
  },

  getProductById: async (id: string): Promise<Product> => {
    try {
      const res = await apiClient.get(`/products/${id}`);
      const raw = res.data?.product || res.data;
      if (raw) return mapProduct(raw);
      throw new Error('Not found');
    } catch (e) {
      const found = MOCK_PRODUCTS.find(p => p.id === id);
      return found || MOCK_PRODUCTS[0];
    }
  },
};
