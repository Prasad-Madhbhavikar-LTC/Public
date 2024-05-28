import {
  Component,
  OnInit,
  Renderer2,
  HostListener,
  Inject
} from '@angular/core';

// import { RouterOutlet } from '@angular/router';
import { Location, DOCUMENT } from "@angular/common";
import { setTheme } from 'ngx-bootstrap/utils';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})

export class AppComponent implements OnInit {
  title: String = 'LBG Mortgages';

  constructor(
    private renderer: Renderer2,
    public location: Location,
    @Inject(DOCUMENT) document: any
  ) {
    setTheme('bs4');
  }

  @HostListener("window:scroll", ["$event"])
  onWindowScroll(e: any) {
    if (window.pageYOffset > 100) {
      var element = document.getElementById("navbar-top");
      if (element) {
        element.classList.remove("navbar-transparent");
        element.classList.add("bg-primary");
      }
    } else {
      var element = document.getElementById("navbar-top");
      if (element) {
        element.classList.add("navbar-transparent");
        element.classList.remove("bg-primary");
      }
    }
  }
  ngOnInit() {
    this.onWindowScroll(event);
  }
}
