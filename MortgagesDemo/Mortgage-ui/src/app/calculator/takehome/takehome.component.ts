import { DOCUMENT } from '@angular/common';
import { Component, Inject, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { TabsetComponent } from 'ngx-bootstrap/tabs';
import { HttpService } from '../../services/http.service';
import { Payload } from './payload';

@Component({
  selector: 'app-takehome',
  templateUrl: './takehome.component.html',
  styleUrl: './takehome.component.scss'
})
export class TakehomeComponent {
  protected isResultAvailable: boolean = false;

  protected incomeValue!: number;
  protected pensionValue!: number;
  protected pensionPercentage!: number;
  protected loanValue!: number;
  protected isPensionValue: boolean = true;
  protected takeHomePerMonth: number = 0;
  protected budgetAmount: number = 0;
  protected pensionDeduction: number = 0;
  protected taxableIncomeValue: number = 0;
  protected insuaranceValue: number = 0;
  protected isPermanentlyEmployed: boolean = false;


  private currancyPattern: string = '^([0-9]{1,3}(,[0-9]{3})*(\.[0-9]+)?|\.[0-9]+)$';
  private numberPattern: string = '^([0-9]{1,3}(\.[0-9]{1,3})?)$';

  constructor(private httpService: HttpService) { }

  calculatorForm = new FormGroup({
    incomeValue: new FormControl('', [
      Validators.required,
      Validators.minLength(2),
      Validators.pattern(this.currancyPattern),
      Validators.min(0)
    ]),
    pensionValue: new FormControl('', [
      Validators.minLength(2),
      Validators.pattern(this.currancyPattern),
      Validators.min(0)
    ]),
    pensionPercentage: new FormControl('', [
      Validators.minLength(1),
      Validators.pattern(this.numberPattern),
      Validators.min(0),
      Validators.max(100)
    ]),
    loanValue: new FormControl('', [
      Validators.minLength(2),
      Validators.pattern(this.currancyPattern),
      Validators.min(0)
    ])
  });

  onTabChange(selectedTab: String) {
    if (selectedTab === "permanent") {
      this.isPermanentlyEmployed = true;
    } else if (selectedTab === "employed") {
      this.isPermanentlyEmployed = false;
    }
  }

  onPensionChange(selectedTab: String) {
    if (selectedTab === "cash") {
      this.isPensionValue = true;
    } else if (selectedTab === "percent") {
      this.isPensionValue = false;
    }
  }

  submit() {
    this.isResultAvailable = false;
    this.pensionDeduction = this.isPensionValue ? this.pensionValue : (this.pensionPercentage * this.incomeValue / 100);

    let payload: Payload = {
      "gross_income": this.incomeValue,
      "employment_type": this.isPermanentlyEmployed ? "permanent_employment" : "self_employment",
      "student_loan_monthly_payment": this.loanValue || 0
    };

    if (this.isPensionValue) {
      payload["pension_contribution_amount"] = this.pensionValue || 0;
    } else {
      payload["pension_contribution_percentage"] = this.pensionPercentage || 0;
    }

    const that = this;
    this.httpService.post("/mortgage-service/api/v1/calculators/net-income", payload).subscribe({
      next: (response: any) => {
        // const responseJson = { // FIXME: this needs to be picked from the response
        //   "gross_annual_income": 0,
        //   "annual_income": 0,
        //   "monthly_pay": 0,
        //   "pension_deduction": 0,
        //   "taxable_income": 0,
        //   "national_insurance": 0,
        //   "student_loan": 0,
        //   "mortgage_eligible_amount": 0
        // };
        const responseJson = JSON.parse(response);
        that.takeHomePerMonth = responseJson.monthly_pay;
        that.incomeValue = responseJson.annual_income;
        that.pensionDeduction = responseJson.pension_deduction;
        that.taxableIncomeValue = responseJson.taxable_income;
        that.insuaranceValue = responseJson.national_insurance;
        that.loanValue = responseJson.student_loan;
        that.budgetAmount = responseJson.mortgage_eligible_amount;

        this.isResultAvailable = true;
        console.log('Post created successfully:', response);
      },
      error: (error) => {
        console.error('Error creating post:', error);
      },
      complete: () => {
        console.info('HTTP request completed.');
      }
    });

    setTimeout(function () {
      const section = document.getElementById('result');
      section?.scrollIntoView({ behavior: 'smooth', block: 'end', inline: 'nearest' });
    }, 300);
  }
}
