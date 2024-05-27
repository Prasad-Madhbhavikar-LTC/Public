import { KYC } from "./kyc";

export interface Customer {
    readonly firstName: string;
    readonly lastName: string;
    readonly email: string;
    readonly phone:string;
    readonly gender?: string;
    readonly image?: string;
    readonly kyc: KYC;
}