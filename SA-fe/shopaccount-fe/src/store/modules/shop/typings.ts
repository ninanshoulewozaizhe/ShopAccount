import { IShopItem, IShopPreItem } from '@/typing/shops/typings';

export interface State {
   allShops: IShopPreItem[];
   curShop: IShopPreItem | null;
}
