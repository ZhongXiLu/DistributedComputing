import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { TokenService } from '../login/token.service';
@Component({
  selector: 'app-newsfeed',
  templateUrl: './newsfeed.component.html',
  styleUrls: ['./newsfeed.component.css']
})
export class NewsfeedComponent implements OnInit {
  welcome = ""
  public responseHolder : any
  constructor(private http: HttpClient, private tokens: TokenService) {
    const token = tokens.token;
    const headers = new HttpHeaders({
      Authorization: token
});
    this.http.post(
      "http://127.0.0.1:5000/api/users/authentication",
      {
        username: localStorage.getItem('username'),
        token: token,
      }
      
   ).subscribe(
    res => {
      console.log(res);
      this.responseHolder = res
      this.welcome = this.responseHolder.data
    },
    err => {
      console.log("Error occured");
    }
  );
   }

  ngOnInit() {
  }

}
