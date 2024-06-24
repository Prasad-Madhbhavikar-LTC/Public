import { Component } from '@angular/core';

@Component({
  selector: 'app-success',
  standalone: true,
  imports: [],
  templateUrl: './success.component.html',
  styleUrl: './success.component.scss'
})
export class SuccessComponent {
  name: string ="John Doe";
  submit() {
    window.location.href = "http://localhost:4191";
  }

}
