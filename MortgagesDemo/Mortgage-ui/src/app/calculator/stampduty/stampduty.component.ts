import { Component } from '@angular/core';
import { DOCUMENT } from "@angular/common";
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpService } from '../../services/http.service';
import { Payload } from './payload';

@Component({
  selector: 'app-stampduty',
  templateUrl: './stampduty.component.html',
  styleUrl: './stampduty.component.scss'
})
export class StampdutyComponent {

  protected isResultAvailable: boolean = false;
  protected propertyValue!: number;
  protected buyingLocation: string = 'england';
  protected stampDutyFor: string = 'first';
  protected isUKResident: boolean = false;
  protected calculatedStampDuty: number = 0;

  private currancyPattern: string = '^([0-9]{1,3}(,[0-9]{3})*(\.[0-9]+)?|\.[0-9]+)$';

  constructor(private httpService: HttpService) { }

  /*
    stamp-duty
    {
      "purchase_price" : ,
      "region" : ,
      "first_time_buyer" : true,
      "move_home" : true,
      "additional_property" : false,
      "uk_resident" : true
    }

    {
      "stamp_duty_charge" : 123456
    }
  */
  calculatorForm = new FormGroup({
    propertyValue: new FormControl('', [
      Validators.required,
      Validators.minLength(2),
      Validators.pattern(this.currancyPattern),
      Validators.min(0)
    ])
  });

  submit() {
    this.isResultAvailable = false;
    let payload: Payload = {
      "purchase_price": this.propertyValue,
      "region": this.buyingLocation === 'wales' ? "wales" : this.buyingLocation === 'scotland' ? "scotland" : "england_northen_ireland",
      "first_time_buyer": this.stampDutyFor === "first",
      "move_home": this.stampDutyFor === "move",
      "additional_property": this.stampDutyFor === "second",
      "uk_resident": this.isUKResident
    };

    const that = this;
    this.httpService.post("/mortgage-service/api/v1/calculators/stamp-duty", payload).subscribe({
      next: (response: any) => {
        // const responseJson = { // FIXME: this needs to be picked from the response
        //   "stamp_duty_charge" : 123456
        // };
        const responseJson = JSON.parse(response);
        that.calculatedStampDuty = responseJson.stamp_duty_charge;
        that.isResultAvailable = true;
        console.log('Post created successfully:', response);
        setTimeout(function () {
          const section = document.getElementById('result');
          section?.scrollIntoView({ behavior: 'smooth', block: 'end', inline: 'nearest' });
        }, 300);
      },
      error: (error) => {
        console.error('Error creating post:', error);
      },
      complete: () => {
        console.info('HTTP request completed.');
      }
    });
  }

  onResidentChange(selectedTab: String) {
    this.isResultAvailable = false;
    if (selectedTab === "resident") {
      this.isUKResident = true;
    } else if (selectedTab === "nonResident") {
      this.isUKResident = false;
    }
  }

  onLocationChange(selectedTab: string) {
    this.isResultAvailable = false;
    if (selectedTab === "england") {
      this.buyingLocation = selectedTab;
    } else if (selectedTab === "scotland") {
      this.buyingLocation = selectedTab;
    } else if (selectedTab === "wales") {
      this.buyingLocation = selectedTab;
    }
  }

  onStampDutyTypeChange(selectedTab: string) {
    this.isResultAvailable = false;
    if (selectedTab === "first") {
      this.stampDutyFor = selectedTab;
    } else if (selectedTab === "second") {
      this.stampDutyFor = selectedTab;
    } else if (selectedTab === "move") {
      this.stampDutyFor = selectedTab;
    }
  }
}
