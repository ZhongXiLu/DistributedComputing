import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent implements OnInit {
  public responseHolder :any
  public users = []
  constructor(private http: HttpClient) { 
    this.http.post('http://127.0.0.1:5000/api/users/all', {
      username: '',
      password: '',
    }).subscribe(
      res => {
        
        this.responseHolder = res
        this.responseHolder.users.forEach(element => {
          this.users.push(element.username);
          console.log(element.username)
      });
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
