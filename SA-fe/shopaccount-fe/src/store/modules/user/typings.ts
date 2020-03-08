export interface State {
    user: IUserInfo | null;
}

export interface IUserInfo {
    id: number;
    username: string;
    email: string;
}
