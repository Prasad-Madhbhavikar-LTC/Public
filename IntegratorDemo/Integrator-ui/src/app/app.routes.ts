import { Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { CatalogueComponent } from './catalogue/catalogue.component';
import { SuccessComponent } from './success/success.component';
import {LoginComponent } from './icici/login/login.component';

export const routes: Routes = [
  { path: "", redirectTo: "login", pathMatch: "full" },
  { path: "login", component: LoginComponent},
  { path: "validate", component: AppComponent },
  { path: "services", component: CatalogueComponent },
  { path: "success", component: SuccessComponent },

];
