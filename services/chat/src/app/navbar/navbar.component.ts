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
  public userId = localStorage.getItem("id");

  constructor(private http: HttpClient, private router:Router, public nav: Navbar) {

  }

  logout(){
    this.router.navigate(['/login']);
    localStorage.clear();
  }

  ngOnInit() {

  }

}
