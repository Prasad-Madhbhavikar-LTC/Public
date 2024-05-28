import { Component } from '@angular/core';
import { NgIf } from '@angular/common';
import { Customer } from './customer';
import { AccountDataService } from '../services/account-data.service';

@Component({
  selector: 'app-customer',
  standalone: true,
  imports: [NgIf],
  templateUrl: './customer.component.html',
  styleUrl: './customer.component.scss'
})
export class CustomerComponent {
  private defaultUser: Customer = {
    firstName: 'Jhon',
    lastName: 'Doe',
    email: 'john.doe@nobody.me',
    phone: '+000000000000',
    // gender: 'unknown',
    image: '../../assets/images/profile-circle.svg',
    kyc: {
      country: 'IN',
      aadharDetails: '0000 0000 0000',
      pan: 'ABCDE0123F',
      address: {
        address1: 'Some Location',
        address2: 'Some Street',
        city: 'Some City',
        state: 'Some State',
        pincode: '000000'
      }
    }
  };

  protected user: Customer = this.defaultUser;
  constructor(private dataService : AccountDataService){}

  ngOnInit(): void {
    this.dataService.customerName = this.user.firstName + ' ' + this.user.lastName;
  }
}
