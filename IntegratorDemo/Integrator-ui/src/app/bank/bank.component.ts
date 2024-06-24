import { Component, Inject } from '@angular/core';
import { Bank } from './bank';
import { AccountDataService } from '../services/account-data.service';
import { CommonModule, DOCUMENT } from '@angular/common';
import { ActivatedRoute, NavigationExtras, Router } from '@angular/router';

declare var $: any;

@Component({
  selector: 'app-bank',
  standalone: true,
  imports: [CommonModule],
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
  protected destinationBank: Bank = this.defaultLBG;
  protected kycStatus: number = 0;
  protected kycStatusDescription: string = "";
  protected statusText: string = "";
  protected whatNext: any = [];
  protected possibleReasons: any = [];

  constructor(private dataService: AccountDataService, @Inject(DOCUMENT) document: any, private router: Router, private route: ActivatedRoute) {
    this.route.queryParams.subscribe(params => {
      this.kycStatus = parseInt(params['k']) || 0;
    });
   }

  ngOnInit(): void {
    this.dataService.integrationID = this.destinationBank.integrationID;
    let that = this;
    setTimeout(function () {
      let link = document.getElementById("services-link");
      if (that.kycStatus == 0){
        that.kycStatus = 1;
      }
      if (that.kycStatus == 1) {
        link?.classList.remove('disabled-link');
      }
    }, 10000);

  }

  getKycStatusText(status: number): string {
    if (this.dataService.kycStatus === 1){
      status = 1;
    }
    switch (status) {
      case 0:
        this.statusText = 'In Progress';
        this.kycStatusDescription = "Your KYC (Know Your Customer) verification is currently in progress. This means we are still reviewing the information you provided. This process ensures we have the most accurate and up-to-date details about you, helping us protect your account and comply with regulatory requirements.";
        this.whatNext = [
          "Please be patient as we complete our checks. This usually takes a few business days.",
          "If we need any additional information, we will contact you via email or phone.",
          "For any urgent queries, feel free to reach out to our support team at 0345 300 0000 or visit our Contact Us page."
        ]
        this.possibleReasons = [];
        break;
      case 1:
        this.statusText = 'Approved';
        this.kycStatusDescription = "Sit Back relax while we take care of the rest!";
        this.whatNext = [
          "No action is required from you side!"
        ]
        this.possibleReasons = [];
        this.dataService.kycStatus = 1;
        $('#kycHelp').modal('hide');
        this.router.navigate(['/lbg/offerings'], {
          queryParams: {
            "s": 1
          }
        });

        break;
      case -1:
        this.statusText = 'Declined';
        this.kycStatusDescription = "Unfortunately, your KYC verification has been declined. This could be due to discrepancies in the information provided or missing documentation.";
        this.whatNext = [
          "Review the information and documents you submitted.",
          "Ensure all details are accurate and up-to-date.",
          "For further assistance, reach out to our support team at 0345 300 0000 or visit our Contact Us page."
        ]
        this.possibleReasons = [
          "Incorrect or incomplete information submitted.",
          "Documents provided do not meet our verification standards."
        ]
        break;
      default:
        this.statusText = 'Contact Support';
        this.kycStatusDescription = "We need some additional information to complete your KYC verification. This is a standard procedure to ensure we have all the necessary details to verify your identity.";
        this.whatNext = [
          "Please contact our support team to provide the required information.",
          "You can reach our team at 0345 300 0000 or visit our Contact Us page."
        ];
        this.possibleReasons = [];
    }
    return this.statusText;
  }


  showKycHelp() {
    if (this.kycStatus != 1) {
      $('#kycHelp').modal('show');
    }
  };

}
