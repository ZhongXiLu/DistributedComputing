import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';
import { Navbar} from '../navbar';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  public responseHolder :any
  public notifications = [];
  public notificationsLength = 0;
  constructor(private http: HttpClient, private router:Router, public nav: Navbar) { 
    const id = localStorage.getItem('id');
    const token = localStorage.getItem("token")
    const encoded = btoa(token.toString()+(':k').toString())
    let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
    this.http.get(environment.notificationServiceUrl+'/notifications/user/'+id, { headers:headers}).subscribe(
      res => {
        this.responseHolder = res;
	this.notifications = this.responseHolder.data.notifications;
	console.log(this.responseHolder);
        this.notificationsLength = this.notifications.length;
      },
      err => {
        console.log(err);
      }
    );
  }
  logout(){
    this.router.navigate(['/login']);
    localStorage.clear();
  }

  ngOnInit() {
  }

  read(id){
    const token = localStorage.getItem("token")
    const encoded = btoa(token.toString()+(':k').toString())
    let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
    this.http.put(environment.notificationServiceUrl+'/notifications/'+id,{ hello:"hi"}, { headers:headers}).subscribe(
      res => {
	console.log(res);
      },
      err => {
        console.log(err);
      }
    );
  }


}
