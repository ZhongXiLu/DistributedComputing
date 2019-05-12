import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { TokenService } from './token.service';
import { tokenKey } from '@angular/core/src/view';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  public token
  public responseHolder :any
  constructor(private http: HttpClient, private router:Router, private tokens: TokenService){
    
  } 

  ngOnInit() {
  }

  submit(event){
    event.preventDefault();
    const password = (<HTMLInputElement>document.getElementById("inputPassword")).value;
    const username = (<HTMLInputElement>document.getElementById("inputUsername")).value;
    // TODO: make username email
    this.http.post(environment.userServiceUrl + '/login', {
      email: username,
      password: password
    }).subscribe(
      res => {
        console.log(res);
	this.responseHolder = res;
	localStorage.setItem('token', this.responseHolder.token);
        localStorage.setItem('id', this.responseHolder.user_id);
        
        this.router.navigate(['/newsfeed']);
        
      },
      err => {
        console.log(err);
      }
    );

  } 

}

