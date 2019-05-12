import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent implements OnInit {
  public responseHolder :any
  public users = [];
  constructor(private http: HttpClient) { 
    this.http.get(environment.userServiceUrl+'/users').subscribe(
      res => {
        this.responseHolder = res;
	this.users = this.responseHolder.data.users;
	console.log(this.users);
      },
      err => {
        console.log("Error occured");
      }
    );
  }

  ngOnInit() {
    
  }

  submit(event){
    const username = event.target.value;
    this.http.post('http://127.0.0.1:5000/api/users/delete', {
      username: username
    }).subscribe(
      res => {
        console.log(res);
        },
      err => {
        console.log("Error occured");
      }
    );

  } 

}
