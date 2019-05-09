import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
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

 follow(id){
    	const follower = localStorage.getItem("id")
   	let headers: HttpHeaders = new HttpHeaders();
    	headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    	headers.append('Authorization', localStorage.getItem("token"));
        this.http.post(environment.followServiceUrl + '/follow', {
        follower_id: follower,
        followee_id: id
    }, { headers}).subscribe(
      res => {
        console.log(res);
      },
      err => {
        console.log(err);
      }
    );
   }

}
