export interface IkindToStocks {
    [index: string]: number;
}

export interface ISuggestObj {
    value: string;
}

export interface IProductDetailItem {
    id: number;
    name: string;
    description: string;
    img: any;
    salesVolumes: number;
    type: IkindToStocks;
}
