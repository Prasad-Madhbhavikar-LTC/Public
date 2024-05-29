import { Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { CatalogueComponent } from './catalogue/catalogue.component';
import { SuccessComponent } from './success/success.component';

export const routes: Routes = [
  { path: "", redirectTo: "validate", pathMatch: "full" },
  { path: "validate", component: AppComponent },
  { path: "services", component: CatalogueComponent },
  { path: "success", component: SuccessComponent },

];
