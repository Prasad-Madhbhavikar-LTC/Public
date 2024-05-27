import { Address } from "../interfaces/address";

export interface Branch {
    readonly branch: string;
    readonly address?: Address;
    readonly ifsc: string;
}