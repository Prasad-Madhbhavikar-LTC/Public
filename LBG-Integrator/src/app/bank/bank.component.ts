import { Component, Inject } from '@angular/core';
import { Bank } from './bank';
import { AccountDataService } from '../services/account-data.service';
import { DOCUMENT } from '@angular/common';

@Component({
  selector: 'app-bank',
  standalone: true,
  imports: [],
  templateUrl: './bank.component.html',
  styleUrl: './bank.component.scss'
})
export class BankComponent {
  protected defaultSourceBank: Bank = {
    name: 'Some Source Bank of India',
    micr: '100100001',
    pan: 'ZYXWV9876U',
    branchDetails: {
      branch: 'Somewhere in India',
      ifsc: 'BANK0000001',
      address: {
        address1: 'Some Bank Location',
        address2: 'Near Some Street',
        city: 'Some City',
        state: 'Some State',
        pincode: '000001'
      }
    },
    accountNumber: '123456789012345',
    accountType: 'Savings',
    services: [
      'Demat Account',
      'Vehicle Loan Account',
      'Credit Card',
      'FD Account'
    ]
  };

  protected defaultLBG: Bank = {
    name: 'Lloyds Banking Group',
    micr: '200300303',
    pan: 'ZYXWV5432G',
    integrationID: '234-jdhhdf-9876rt45',
    branchDetails: {
      branch: 'Somewhere in UK',
      ifsc: 'BANK0000002',
      address: {
        address1: 'Some UK Bank Location',
        address2: 'Near Some UK Street',
        city: 'Some City in UK',
        state: 'Some State in UK',
        pincode: '000002'
      }
    },
  };

  protected sourceBank: Bank = this.defaultSourceBank;
  protected destinationBank : Bank = this.defaultLBG;
  protected kycStatus : number = 0;
  constructor(private dataService : AccountDataService, @Inject(DOCUMENT) document: any){}

  ngOnInit(): void {
    this.dataService.integrationID = this.destinationBank.integrationID ;
    let that = this;
    setTimeout(function () {
      let link = document.getElementById("services-link");
      let bttn = document.getElementById("submitButton");
      that.kycStatus = 1;
      link?.classList.remove('disabled-link');
    }, 5000);

  }


}
