import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { TokenService } from './token.service';
import { tokenKey } from '@angular/core/src/view';

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
    this.http.post('http://127.0.0.1:5000/api/users/token', {
      username: username,
      password: password
    }).subscribe(
      res => {
        this.token = res;
        this.responseHolder = res
        console.log(this.responseHolder.response);
        this.tokens.token = this.responseHolder.response
        localStorage.setItem('username', username);
        if (this.responseHolder.admin==""){
          this.router.navigate(['/']);
        }
        else
        {
          this.router.navigate(['/admin']);
        }
        
      },
      err => {
        console.log("Error occured");
      }
    );

  } 

}

