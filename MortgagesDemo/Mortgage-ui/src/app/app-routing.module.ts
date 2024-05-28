import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CommonModule } from "@angular/common";
import { BrowserModule } from "@angular/platform-browser";

import { HomeComponent } from './home/home.component';
import { MortgageComponent } from './calculator/mortgage/mortgage.component';
import { StampdutyComponent } from './calculator/stampduty/stampduty.component';
import { TakehomeComponent } from './calculator/takehome/takehome.component';

const routes: Routes = [
  { path: "", redirectTo: "home", pathMatch: "full" },
  { path: "home", component: HomeComponent },
  { path: "calculator/mortgage", component: MortgageComponent},
  { path: "calculator/stampduty", component: StampdutyComponent},
  { path: "calculator/takehome", component: TakehomeComponent}
];

@NgModule({
  imports: [
    CommonModule,
    BrowserModule,
    RouterModule.forRoot(routes, {
    useHash: true
  })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
