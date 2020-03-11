import { IndexOJ } from '../productDetail/typings';

export interface SalesRecordItem {
    id: number;
    name: string;
    pid: number;
    sid: number;
    date: string;
    sales: IndexOJ;
    salesVolumes?: number;
}

export interface OneDaySalesItem {
    date: string;
    sales: IndexOJ;
}
