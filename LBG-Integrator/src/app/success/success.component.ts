import { Component } from '@angular/core';
import { AccountDataService } from '../services/account-data.service';

@Component({
  selector: 'app-success',
  standalone: true,
  imports: [],
  templateUrl: './success.component.html',
  styleUrl: './success.component.scss'
})
export class SuccessComponent {
  protected userName ?: string;
  protected accountNumber ?: string;
  protected applicationId ?: string; 

  constructor (private dataService : AccountDataService){
    this.applicationId = this.dataService.integrationID;
    this.userName = this.dataService.customerName;
    this.accountNumber = this.dataService.accountNumber;
  }

}
