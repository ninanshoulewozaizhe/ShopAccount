import { IndexOJ } from '../productDetail/typings';

export interface SalesRecordItem {
    id: number;
    name: string;
    pid: number;
    sid: number;
    date: string;
    sales: IndexOJ | string;
    salesVolumes?: number;
}

export interface ShopsSalesItem {
    [index: string]: SalesRecordItem[];
}

export interface ShopSalesChartData {
    columns: string[];
    rows: ShopSalesChartRowItem[];
}
export interface ShopSalesChartRowItem {
    店铺: string;
    销量: number;
}
