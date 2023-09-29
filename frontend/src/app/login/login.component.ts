import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { SharedService } from '../shared.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit{

  constructor(private router: Router, private sharedService: SharedService) {}

  ngOnInit(): void {
    // Determine if the user is on the login page
    const isLoginPage = this.router.url.includes('login');
    this.sharedService.setIsLoginPage(isLoginPage);
  }

}
