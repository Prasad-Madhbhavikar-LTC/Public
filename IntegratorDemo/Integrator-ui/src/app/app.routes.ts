import { Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { CatalogueComponent } from './catalogue/catalogue.component';
import { SuccessComponent } from './success/success.component';

export const routes: Routes = [
  { path: "", redirectTo: "/lbg/validate", pathMatch: "full" },
  { path: "lbg/validate", component: AppComponent },
  { path: "lbg/offerings", component: CatalogueComponent },
  { path: "lbg/status", component: SuccessComponent },

];
