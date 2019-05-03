import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  public username : string;
  constructor(private http: HttpClient) 
{
   }

  ngOnInit() {
const username = localStorage.getItem('username');
	console.log(username);
	this.http.get('http://localhost:5001/users/name/'+'test1').subscribe(
        res => {
        console.log(res);
	this.username = res.data.username;
	console.log(this.username);
      },
      err => {
        console.log(err);
      }); 
  }

}
