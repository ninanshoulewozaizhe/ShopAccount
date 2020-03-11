import { IProductDetailItem } from '@/typing/productDetail/typings';

export interface State {
   allProducts: IProductDetailItem[];
   curShopProducts: IProductDetailItem[];
   curProduct: IProductDetailItem | null;
}
