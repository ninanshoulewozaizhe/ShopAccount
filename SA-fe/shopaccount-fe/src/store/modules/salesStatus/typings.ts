import { SalesRecordItem, OneDaySalesItem } from '@/typing/salesStatus/typings';


export interface State {
    curShopTodaySales: SalesRecordItem[];
    curShopPeriodSales: OneDaySalesItem[];
}
