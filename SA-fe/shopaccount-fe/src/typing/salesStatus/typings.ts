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
