import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  public responseHolder :any
  public notifications = [];
  constructor(private http: HttpClient) { 
    const id = localStorage.getItem('id');
    this.http.get(environment.notificationServiceUrl+'/notifications/user/'+id).subscribe(
      res => {
        this.responseHolder = res;
	this.notifications = this.responseHolder.data.notifications;
	console.log(this.responseHolder);
      },
      err => {
        console.log("Error occured");
      }
    );
  }

  ngOnInit() {
  }

}
