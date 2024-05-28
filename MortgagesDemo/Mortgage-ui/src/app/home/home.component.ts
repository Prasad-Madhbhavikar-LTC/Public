import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router, NavigationExtras } from '@angular/router';

// import { AppRoutingStateService } from '../app-routing-state.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  private reMOrtgagePlaceholderAmount: number = 280000;
  private purchasePlaceholderAmount: number = 20000;
  private calculatorTabSeleted: String = "m";

  protected textboxlabel: String = "My house deposit";
  protected placeholderAmount: number = this.purchasePlaceholderAmount;

  protected incomeValue!: number;
  protected propertyValue!: number;

  protected isFormValid = true;

  calculatorForm = new FormGroup({
    incomeValue: new FormControl('', [
      Validators.required,
      Validators.minLength(2),
      Validators.pattern('^([0-9]{1,3}(,[0-9]{3})*(\.[0-9]+)?|\.[0-9]+)$'),
      Validators.min(0)
    ]),
    propertyValue: new FormControl('', [
      Validators.required,
      Validators.minLength(2),
      Validators.pattern('^([0-9]{1,3}(,[0-9]{3})*(\.[0-9]+)?|\.[0-9]+)$'),
      Validators.min(0)
    ])
  });

  // this.form.get('incomeValue');
  constructor(private router: Router) { }

  onTabChange(selectedTab: String) {
    if (selectedTab === "purchase") {
      this.textboxlabel = "My house deposit";
      this.placeholderAmount = this.purchasePlaceholderAmount;
      // this.appRoutingStateService.setSharedStateData("routeId", selectedTab);
      this.calculatorTabSeleted = 'm';
    } else if (selectedTab === "remortgage") {
      this.textboxlabel = "I have saved up a deposit of";
      this.placeholderAmount = this.reMOrtgagePlaceholderAmount;
      // this.appRoutingStateService.setSharedStateData("routeId", selectedTab);
      this.calculatorTabSeleted = 'r';
    }
  }

  submit() {
    const navigationExtras: NavigationExtras = {
      queryParams: {
        t: this.calculatorTabSeleted,
        i: this.incomeValue,
        p: this.propertyValue
      }
    };

    if (this.calculatorForm.valid) {
      this.router.navigate(['/calculator/mortgage'], navigationExtras);
    }
  }
}
