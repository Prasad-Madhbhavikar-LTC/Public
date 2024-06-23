import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { AccountComponent } from './account/account.component';
import { SuccessComponent } from './success/success.component';


export const routes: Routes = [
    { path: "", redirectTo: "icici/login", pathMatch: "full" },
    { path: "icici/login", component: LoginComponent },
    { path: "icici/account", component: AccountComponent },
    { path: "icici/redirect", component: SuccessComponent },
  ];
  