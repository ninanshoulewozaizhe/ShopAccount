export interface IkindToStocks {
    [index: string]: number;
}

export interface ISuggestObj {
    value: string;
}

export interface IndexOJ {
    [index: string]: number;
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
    cost?: number;
    price?: number;
}

export interface IProductSalesItem {
    type: string;
    amount: number;
    disable: boolean;
}
