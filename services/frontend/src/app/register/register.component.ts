import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';
import { Navbar} from '../navbar';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  public errorMessage : any
  constructor(private http: HttpClient, private router: Router, public nav: Navbar) {

  }

  ngOnInit() {
    this.nav.hide();
  }

  submit(event) {
    event.preventDefault();
    const password = (<HTMLInputElement>document.getElementById('inputPassword')).value;
    const username = (<HTMLInputElement>document.getElementById('inputUsername')).value;
    const email = (<HTMLInputElement>document.getElementById('inputEmail')).value;
    this.http.post(environment.userServiceUrl + '/users', {
      username: username,
      email: email,
      password: password
    }).subscribe(
      res => {
        console.log(res);
        this.router.navigate(['/login']);
      },
      err => {
        this.errorMessage = err.error;
        console.log(err);
        const danger = (<HTMLInputElement>document.getElementById("danger"));
        danger.innerHTML=this.errorMessage.message;
      }
    );

  }

}
