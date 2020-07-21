export interface IShopItem {
    id: number;
    uid: number;
    img?: string;
    name: string;
    description?: string;
    salesVolumes: number;
    productAmount: number;
}

export interface IShopPreItem {
    id: number;
    uid: number;
    img?: string;
    name: string;
    description?: string;
    salesVolumes: number;
    productAmount: number;
    preProductImgs?: string[];
}
