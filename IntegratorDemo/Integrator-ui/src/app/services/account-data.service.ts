import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AccountDataService {

  private _customerName?: string | undefined;

  public get customerName(): string | undefined {
    return this._customerName;
  }

  public set customerName(value: string | undefined) {
    this._customerName = value;
  }

  private _accountNumber?: string | undefined;

  public get accountNumber(): string | undefined {
    return this._accountNumber;
  }

  public set accountNumber(value: string | undefined) {
    this._accountNumber = value;
  }

  private _integrationID?: string | undefined;

  public get integrationID(): string | undefined {
    return this._integrationID;
  }

  public set integrationID(value: string | undefined) {
    this._integrationID = value;
  }

  private _kycStatus: number = -1;

  public get kycStatus(): number {
    return this._kycStatus;
  }

  public set kycStatus(value: number) {
    this._kycStatus = value;
  }

  constructor() { }
}
