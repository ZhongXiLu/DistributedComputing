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
    this.http.delete(environment.userServiceUrl+'/users/'+id, { headers:headers}).subscribe(
      res => {
        console.log(res);
        const success = (<HTMLInputElement>document.getElementById("success"));
        success.innerHTML="User deleted";
        },
      err => {
        console.log(err);
      }
    );

  } 

  block(id){
    this.http.put(environment.userServiceUrl+'/users/'+id+'/block').subscribe(
      res => {
        console.log(res);
        const success = (<HTMLInputElement>document.getElementById("success"));
        success.innerHTML="User blocked";
        },
      err => {
        console.log(err);
      }
    );

  } 

 unblock(id){
    this.http.put(environment.userServiceUrl+'/users/'+id+'/unblock').subscribe(
      res => {
        console.log(res);
        const success = (<HTMLInputElement>document.getElementById("success"));
        success.innerHTML="User unblocked";
        },
      err => {
        console.log(err);
      }
    );

  }

}
