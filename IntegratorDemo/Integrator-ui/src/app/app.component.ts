import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ActivatedRoute, NavigationExtras, Router, RouterModule, Routes } from '@angular/router';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { CatalogueComponent } from './catalogue/catalogue.component';
import { BankComponent } from './bank/bank.component';
import { CustomerComponent } from './customer/customer.component';
import { CommonModule } from '@angular/common';
import { SuccessComponent } from './success/success.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterModule, CommonModule, HeaderComponent, CatalogueComponent, CustomerComponent, BankComponent, SuccessComponent, FooterComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'LBG Integrator';
  integrationId: string = 'xx1234er875990237';
  selectedStep: number = 0;

  constructor(private route: ActivatedRoute, private router: Router) {
    this.route.queryParams.subscribe(params => {
      this.selectedStep = parseInt(params['s']) || 0;
    });
  }

  next(selectedStep: number) {
    this.selectedStep = selectedStep;
    // const navigationExtras: NavigationExtras = {
    //   queryParams: {
    //     s: this.selectedStep
    //   }
    // };
    // this.router.navigate([''], navigationExtras);
  }
}
