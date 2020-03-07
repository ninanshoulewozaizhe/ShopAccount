export interface State {
    user: IUserInfo | null;
}

export interface IUserInfo {
    uid: number;
    username: string;
    email: string;
}
