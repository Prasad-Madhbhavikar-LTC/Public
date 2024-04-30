import { DOCUMENT } from '@angular/common';
import { Component, Inject, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { TabsetComponent } from 'ngx-bootstrap/tabs';
import { HttpService } from '../../services/http.service';

@Component({
  selector: 'app-mortgage',
  templateUrl: './mortgage.component.html',
  styleUrl: './mortgage.component.scss'
})
export class MortgageComponent {
  @ViewChild('mortgageType', { static: false }) mortgageType!: TabsetComponent;

  protected isMortgagaRoute: boolean = true;
  private reMOrtgagePlaceholderAmount: number = 280000;
  private purchasePlaceholderAmount: number = 20000;
  private controlDelay: number = 50;

  protected textboxlabel: String = "My house deposit";
  protected placeholderAmount: number = this.purchasePlaceholderAmount;

  protected isResultAvailable: boolean = false;
  protected isMortgageAllowed: boolean = true;
  protected isBuyerSelected: boolean = false;
  protected ispropertySelected: boolean = false;
  protected isBoosterSelected: boolean = false;
  protected isMortgageSelected: boolean = false;

  protected incomeValue!: number;
  protected propertyValue!: number;
  protected propertyPrice!: number;
  protected boosterIncome!: number;
  protected boosterSavings!: number;
  protected boosterValue!: number;
  protected mortgageBalance!: number;
  protected mortgageBorrowing!: number;


  // values are reset every time the tab is changed
  protected finalBestValue: number = 0;
  protected partBuyPartRentEstimate: number = 0;
  protected partBuyPartRate: number = 0;
  protected partBuyPartMonthly: number = 0;
  protected standardEstimate: number = 0;
  protected standardRate: number = 0;
  protected standardMonthly: number = 0;
  protected boosterEstimate: number = 0;
  protected boosterRate: number = 0;
  protected boosterMonthly: number = 0;
  protected familyRemortgageEstimate: number = 0;
  protected familyRemortgageRate: number = 0;
  protected familyRemortgageMonthly: number = 0;

  private currancyPattern: string = '^([0-9]{1,3}(,[0-9]{3})*(\.[0-9]+)?|\.[0-9]+)$';

  calculatorForm = new FormGroup({
    incomeValue: new FormControl('', [
      Validators.required,
      Validators.minLength(2),
      Validators.pattern(this.currancyPattern),
      Validators.min(0)
    ]),
    propertyValue: new FormControl('', [
      Validators.required,
      Validators.minLength(2),
      Validators.pattern(this.currancyPattern),
      Validators.min(0)
    ]),
    propertyPrice: new FormControl('', [
      Validators.minLength(2),
      Validators.pattern(this.currancyPattern),
      Validators.min(0)
    ]),
    mortgageBalance: new FormControl('', [
      Validators.minLength(2),
      Validators.pattern(this.currancyPattern),
      Validators.min(0)
    ]),
    mortgageBorrowing: new FormControl('', [
      Validators.minLength(2),
      Validators.pattern(this.currancyPattern),
      Validators.min(0)
    ]),
    boosterIncome: new FormControl('', [
      Validators.minLength(2),
      Validators.pattern(this.currancyPattern),
      Validators.min(0)
    ]),
    boosterSavings: new FormControl('', [
      Validators.minLength(2),
      Validators.pattern(this.currancyPattern),
      Validators.min(0)
    ]),
    boosterValue: new FormControl('', [
      Validators.minLength(2),
      Validators.pattern(this.currancyPattern),
      Validators.min(0)
    ])
  });

  constructor(@Inject(DOCUMENT) document: any, private route: ActivatedRoute, private httpService: HttpService) {
    this.route.queryParams.subscribe(params => {
      this.isMortgagaRoute = params['t'] === 'm';
      this.incomeValue = params['i'];
      this.propertyValue = params['p'];

      if (params['t'] === 'r' || params['t'] === 'm') {
        var that = this;

        setTimeout(function () {
          that.selectCorrectMortgageTab();
          console.log("Tab change triggered");
        }, this.controlDelay);

        if (this.incomeValue > 0 && this.propertyValue > 0) {

          setTimeout(function () {
            console.log("Submit triggered");
            that.submit();
          }, this.controlDelay + 50);
        }
      } else {

      }
    });
  }


  onTabChange(selectedTab: String) {
    if (selectedTab === "purchase") {
      this.textboxlabel = "I have saved up a deposit of";
      this.placeholderAmount = this.purchasePlaceholderAmount;
      this.isMortgagaRoute = true;
    } else if (selectedTab === "remortgage") {
      this.textboxlabel = "Property Value";
      this.placeholderAmount = this.reMOrtgagePlaceholderAmount;
      this.isMortgagaRoute = false;
    }
    this.resetValues();
  }

  submit() {
    let payload = {};
    this.isResultAvailable = false;
    this.isBoosterSelected = (this.boosterIncome > 0 || this.boosterSavings > 0 || this.boosterValue > 0)
    this.ispropertySelected = (this.propertyPrice > 0);
    this.isBuyerSelected = (this.incomeValue > 0 || this.propertyValue > 0);
    this.isMortgageSelected = (this.mortgageBalance > 0 || this.mortgageBorrowing > 0);
    if (this.isMortgagaRoute) {
      payload = {
        "purpose": "purchase",
        "customer": {
          "income": this.incomeValue,
          "saving": this.propertyValue
        },
        "property_price": this.propertyPrice || 0,
        "booster": {
          "income": this.boosterIncome || 0,
          "saving": this.boosterSavings || 0,
          "property-value": this.boosterValue || 0
        }
      }
    } else {
      payload = {
        "purpose": "remortgage",
        "customer": {
          "income": this.incomeValue
        },

        "property_price": this.propertyValue,
        "booster": {
          "income": this.boosterIncome || 0
        },
        "mortgage_balance": this.mortgageBalance || 0,
        "additional_borrowing": this.mortgageBorrowing || 0
      }

    }

    const that = this;
    this.httpService.post("/mortgage-service/api/v1/calculators/mortgage", payload).subscribe({
      next: (response: any) => {
        const responseJson = JSON.parse(response);
        this.finalBestValue = 0;
        this.isMortgageAllowed = responseJson.eligibility || false;
        responseJson.mortgage_response.forEach(function (obj: any) {
          if (obj.mortgageType.toLowerCase() === "familyremortgage" || obj.mortgageType.toLowerCase() === "interestonlyremortgage") {
            that.familyRemortgageEstimate = obj.mortgageAmount;
            that.familyRemortgageMonthly = obj.monthlyPay;
            that.familyRemortgageRate = obj.interestRate;

            if (that.finalBestValue < obj.mortgageAmount) {
              that.finalBestValue = obj.mortgageAmount;
            }
          }

          if (obj.mortgageType.toLowerCase() === "partbuypartrentmortgage" || obj.mortgageType.toLowerCase() === "partandpartremortgage") {
            that.partBuyPartRentEstimate = obj.mortgageAmount;
            that.partBuyPartMonthly = obj.monthlyPay;
            that.partBuyPartRate = obj.interestRate;

            if (that.finalBestValue < obj.mortgageAmount) {
              that.finalBestValue = obj.mortgageAmount;
            }
          }

          if (obj.mortgageType.toLowerCase() === "guarantormortgage" || obj.mortgageType.toLowerCase() === "incomeboostremortgage") {
            that.boosterEstimate = obj.mortgageAmount;
            that.boosterRate = obj.interestRate;
            that.boosterMonthly = obj.monthlyPay;

            if (that.finalBestValue < obj.mortgageAmount) {
              that.finalBestValue = obj.mortgageAmount;
            }
          }

          if (obj.mortgageType.toLowerCase() === "standardmortgage" || obj.mortgageType.toLowerCase() === "standardremortgage") {
            that.standardEstimate = obj.mortgageAmount;
            that.standardMonthly = obj.monthlyPay;
            that.standardRate = obj.interestRate;

            if (that.finalBestValue < obj.mortgageAmount) {
              that.finalBestValue = obj.mortgageAmount;
            }
          }
        });

        this.isResultAvailable = true;
        console.log('Post created successfully:', response);
      },
      error: (error) => {
        console.error('Error creating post:', error);
      },
      complete: () => {
        console.info('HTTP request completed.');
      }
    }
    );
  }

  selectCorrectMortgageTab() {
    let that = this;
    this.isResultAvailable = false;
    setTimeout(() => {
      try {
        that.mortgageType.tabs[that.isMortgagaRoute ? 0 : 1].active = true;
      } catch (e) { }
    }, this.controlDelay);
  }

  scrollToView(id: string) {
    this.isResultAvailable = false;
    this.selectCorrectMortgageTab();
    setTimeout(function () {
      const section = document.getElementById(id);
      section?.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest' });
    }, this.controlDelay + 20);
  }

  resetValues() {
    this.finalBestValue = 0;
    this.partBuyPartRentEstimate = 0;
    this.partBuyPartRate = 0;
    this.partBuyPartMonthly = 0;
    this.standardEstimate = 0;
    this.standardRate = 0;
    this.standardMonthly = 0;
    this.boosterEstimate = 0;
    this.boosterRate = 0;
    this.boosterMonthly = 0;
    this.familyRemortgageEstimate = 0;
    this.familyRemortgageRate = 0;
    this.familyRemortgageMonthly = 0;
  }
}