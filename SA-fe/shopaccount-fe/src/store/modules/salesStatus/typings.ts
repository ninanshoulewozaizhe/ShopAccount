import { SalesRecordItem, ShopsSalesItem } from '@/typing/salesStatus/typings';
import { IProductDetailItem } from '@/typing/productDetail/typings';

export interface State {
    curShopTodaySales: SalesRecordItem[];
    curShopPeriodSales: SalesRecordItem[];
    curProductTodaySales: SalesRecordItem | null;
    curProductYesterdaySales: SalesRecordItem | null;
    productOneDaySales: SalesRecordItem | null;
    curProductPeriodSales: SalesRecordItem[];
    allShopsTodaySales: ShopsSalesItem | null;
    productsSalesRank: IProductDetailItem[];
}
