import { Component } from '@angular/core';
import { SharedService } from './shared.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  // title = 'frontend';

  isLoginPage: boolean = true; // Set to true by default

  constructor(private sharedService: SharedService) {}

  ngOnInit(): void {
    this.sharedService.isLoginPage$.subscribe(isLoginPage => {
      this.isLoginPage = isLoginPage;
    });
  }

}
