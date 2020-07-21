export interface IkindToStocks {
    [index: string]: number;
}

export interface ISuggestObj {
    value: string;
}

export interface IndexOJ {
    [index: string]: number;
}

export interface IndexStingOJ {
    [index: string]: any;
}

export interface IProductDetailItem {
    id: number;
    name: string;
    description?: string;
    img?: any;
    salesVolumes: number;
    sid: number;
    shop: string;
    type: IkindToStocks;
}

export interface IProductSalesItem {
    type: string;
    amount: number;
    disable?: boolean;
}

export interface SalesChartData {
    columns: string[];
    rows: SalesChartRowItem[];
}
export interface SalesChartRowItem {
    日期: string;
    销量: number;
}
