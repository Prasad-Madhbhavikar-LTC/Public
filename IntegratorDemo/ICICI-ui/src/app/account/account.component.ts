import { Component } from '@angular/core';
import { NavigationExtras, Router } from '@angular/router';

@Component({
  selector: 'app-account',
  standalone: true,
  imports: [],
  templateUrl: './account.component.html',
  styleUrl: './account.component.scss'
})
export class AccountComponent {
  name: string ="John Doe";
  constructor(private router: Router) { }

  submit(): void {
    const navigationExtras: NavigationExtras = {
      queryParams: {

      }
    };

    if (true) {
      this.router.navigate(['/icici/redirect'], navigationExtras);
    }
  }
}
