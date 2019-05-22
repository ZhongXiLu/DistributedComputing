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
  public statsDays = [];
  public numberUsers = 0;
  public environment = environment;
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
        this.statsDays = Object.keys(this.stats);
      },
      err => {
        console.log("Error occured");
      }
    );
    
  }

  submit(id){
    const token = localStorage.getItem("token")
    const encoded = btoa(token.toString()+(':k').toString())
    let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
    this.http.post(environment.userServiceUrl+'/users', {
      username: username
    }, { headers:headers}).subscribe(
      res => {
        console.log(res);
        },
      err => {
        console.log("Error occured");
      }
    );

  } 

  block(id){
    const token = localStorage.getItem("token")
    const encoded = btoa(token.toString()+(':k').toString())
    let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
    this.http.post(environment.userServiceUrl+'/users', {
      username: username
    },{ headers:headers}).subscribe(
      res => {
        console.log(res);
        },
      err => {
        console.log("Error occured");
      }
    );

  } 

}
