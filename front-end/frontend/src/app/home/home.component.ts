import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { TokenService } from '../login/token.service';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  welcome = ""
  constructor(private http: HttpClient, private tokens: TokenService) {
    const token = tokens.token;
    const headers = new HttpHeaders({
      Authorization: token
});
    this.http.post(
      "http://127.0.0.1:5000/api/users/authentication",
      {
        username: "angela",
        token: token,
      }
      
   ).subscribe(
    res => {
      console.log(res);
      this.welcome = res.data
    },
    err => {
      console.log("Error occured");
    }
  );
   }

  ngOnInit() {
  }

}
