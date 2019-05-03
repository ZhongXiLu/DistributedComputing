import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';

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
        const id = localStorage.getItem('id');
	console.log(id);
	this.http.get('http://localhost:5001/users/'+id).subscribe(
        res => {
        console.log(res);
	const response = res
	this.username = response.data.username;
	console.log(this.username);
      },
      err => {
        console.log(err);
      }); 

      this.http.get(environment.postServiceUrl+'/user/'+id).subscribe(
        res => {
        console.log(res);
      },
      err => {
        console.log(err);
      });
  }

}
