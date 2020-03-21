export interface UserInfo {
    id: number;
    username: string;
    phone: string;
    img?: string;
}

export interface ChangePdForm {
    o_password: string;
    n_password: string;
    n_confirmPd?: string;
}
