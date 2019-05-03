import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { TokenService } from '../login/token.service';
import { environment } from '../../environments/environment';
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

  submit(event){
    event.preventDefault();
    var headers = new Headers();
    headers.append('Authorization', 'Bearer ' + localStorage.getItem("token"));
    headers.append('Content-Type', 'application/json');
    const token = localStorage.getItem('token');
    const creator = localStorage.getItem('id');
    const content =(<HTMLInputElement>document.getElementById("message")).value;
    const tags = (<HTMLInputElement>document.getElementById("tags")).value;
    const tagsArray = [];
    tagsArray = tags.split(',');
    console.log(tagsArray);
    console.log(tagsArray);
    this.http.post(environment.postServiceUrl+'/posts', {
      content: content,
      creator: creator,
      tags: [1,2,3]
    },{ headers: headers }).subscribe(
      res => {
        console.log(res);  
      },
      err => {
        console.log(err);
      }
    );

  } 

}
