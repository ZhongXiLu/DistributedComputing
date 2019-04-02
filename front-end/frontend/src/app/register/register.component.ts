import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  constructor(private http: HttpClient, private router: Router){
    
  } 

  ngOnInit() {
  }

  submit(event){
    event.preventDefault();
    const password = (<HTMLInputElement>document.getElementById("inputPassword")).value;
    const username = (<HTMLInputElement>document.getElementById("inputUsername")).value;
    this.http.post('http://127.0.0.1:5000/api/users/register', {
      username: username,
      password: password
    }).subscribe(
      res => {
        console.log(res);
        this.router.navigate(['/login']);
      },
      err => {
        console.log("Error occured");
      }
    );

  }

}
