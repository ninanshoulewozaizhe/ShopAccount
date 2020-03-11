import { SalesRecordItem, OneDaySalesItem } from '@/typing/salesStatus/typings';


export interface State {
    curShopTodaySales: SalesRecordItem[];
    curShopPeriodSales: OneDaySalesItem[];
    curProductTodaySales: SalesRecordItem | null;
    curProductYesterdaySales: SalesRecordItem | null;
    productOneDaySales: SalesRecordItem | null;
}
