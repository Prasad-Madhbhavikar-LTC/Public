import { Component } from '@angular/core';
import { NavigationExtras, Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  constructor(private router: Router) { }

  submit(): void {
    const navigationExtras: NavigationExtras = {
      queryParams: {

      }
    };

    if (true) {
      this.router.navigate(['/icici/account'], navigationExtras);
    }
  }
}
