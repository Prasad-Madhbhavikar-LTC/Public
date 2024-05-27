import { Component } from '@angular/core';
import { Product } from './product';
import { NgFor } from '@angular/common';
import { FormControl, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HttpService } from '../services/http.service';
import { NavigationExtras, Router } from '@angular/router';
import { AccountDataService } from '../services/account-data.service';

@Component({
  selector: 'app-catalogue',
  standalone: true,
  imports: [NgFor, ReactiveFormsModule],
  templateUrl: './catalogue.component.html',
  styleUrl: './catalogue.component.scss'
})
export class CatalogueComponent {
  protected productOfferings?: Product[] = [
    {
      id: "cur_acc",
      serviceType: "Current Account",
      helpText: "Some help to be displayed here",
      isEnabled: true,
      defaultSelected: true
    },
    {
      id: "sav_acc",
      serviceType: "Savings Account",
      helpText: "Some help to be displayed here",
      isEnabled: false,
      defaultSelected: false
    },
    {
      id: "mor_acc",
      serviceType: "Mortgage Account",
      helpText: "Some help to be displayed here",
      isEnabled: false,
      defaultSelected: false
    },
    {
      id: "cre_acc",
      serviceType: "Credit Card",
      helpText: "Some help to be displayed here",
      isEnabled: false,
      defaultSelected: false
    },
    {
      id: "veh_acc",
      serviceType: "Vehicle Loan",
      helpText: "Some help to be displayed here",
      isEnabled: false,
      defaultSelected: false
    }];

  protected mpinPasswordConfirm?: string;
  protected mpinPassword?: string;
  protected ipinPassword?: string;
  protected ipinPasswordConfirm?: string;
  private integrationID ?: string;


  catalogueForm = new FormGroup({
    mpinPassword: new FormControl('', [
      Validators.required,
      Validators.minLength(2),
      Validators.min(0)
    ]),
    mpinPasswordConfirm: new FormControl('', [
      Validators.required,
      Validators.minLength(2),
      Validators.min(0)
    ]),
    ipinPassword: new FormControl('', [
      Validators.minLength(2),
      Validators.min(0)
    ]),
    ipinPasswordConfirm: new FormControl('', [
      Validators.minLength(2),
      Validators.min(0)
    ])
  });

  // this.catalogueForm.get(‘mpinPasswordConfirm’).value
  constructor(private router: Router, private dataService : AccountDataService) { }
  submit() {
    this.dataService.accountNumber = '8765654456577676';
    const navigationExtras: NavigationExtras = {
      queryParams: {
        s: 2
      }
    };
    this.router.navigate(['/success'], navigationExtras);
  };

  ngOnInit(): void {
    this.integrationID = this.dataService.integrationID;
  }
}
