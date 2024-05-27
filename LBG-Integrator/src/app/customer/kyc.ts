import { Address } from "../interfaces/address";

export interface KYC{
    country: string;
    aadharDetails?: string;
    pan?: string;
    address: Address;
}