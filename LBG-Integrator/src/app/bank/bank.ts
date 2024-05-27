import { Branch } from './branch'

export interface Bank {
    readonly name: string;
    readonly micr: string;
    readonly pan: string;
    readonly image?: string;
    readonly branchDetails: Branch;
    readonly accountNumber?: string;
    readonly accountType?: string;
    readonly services?: string[];
    readonly integrationID?: string;
}