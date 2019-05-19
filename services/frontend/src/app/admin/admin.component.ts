import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Navbar} from '../navbar';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent implements OnInit {
  public responseHolder :any
  public statsHolder :any
  public users = [];
  public stats = [];
  public numberUsers = 0;
  public numberPosts = 0;
  constructor(private http: HttpClient,public nav: Navbar) { 
    this.http.get(environment.userServiceUrl+'/users').subscribe(
      res => {
        this.responseHolder = res;
	this.users = this.responseHolder.data.users;
	console.log(this.users);
	this.numberUsers = this.users.length;
      },
      err => {
        console.log("Error occured");
      }
    );
  }

  ngOnInit() {
    this.nav.show();
    this.http.get(environment.postServiceUrl+'/posts/stats').subscribe(
      res => {
        this.statsHolder = res;
	this.stats = this.statsHolder.data.stats;
	console.log(this.stats);
        this.numberPosts = Object.keys(this.stats).length;
      },
      err => {
        console.log("Error occured");
      }
    );
    
  }

  submit(event){
    const username = event.target.value;
    this.http.post(environment.userServiceUrl+'/users', {
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
