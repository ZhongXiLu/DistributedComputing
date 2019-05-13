import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  public username : string;
  public responseHolder :any;
  public dataHolder :any;
  public posts = [];
  public commentHolder :any;
  public comments = {};
  public try = ["hello","hi"];
  constructor(private http: HttpClient) 
{
   }

  ngOnInit() {
        const id = localStorage.getItem('id');
	console.log(id);
	this.http.get('http://localhost:5001/users/'+id).subscribe(
        res => {
	this.responseHolder = res;
	this.username = this.responseHolder.data.username;
	console.log(this.username);
      },
      err => {
        console.log(err);
      }); 

      this.http.get(environment.postServiceUrl+'/posts/user/'+id).subscribe(
        res => {
        console.log(res);
	this.dataHolder = res;
	this.posts = this.dataHolder.data.posts;
	console.log(this.posts);
	for (let post of this.posts){
	this.http.get(environment.commentServiceUrl+'/comments/posts/'+post.id).subscribe(
        res => {
      	this.commentHolder = res;
	this.comments[post.id]=this.commentHolder.data.comments;
	console.log(this.comments);
	}); 
	}
      },
      err => {
        console.log(err);
      });
 
  }

   submitComment(event){
    	const id= (<HTMLInputElement>document.getElementById("id")).value;
    	const creator = localStorage.getItem("id");
	const comment= (<HTMLInputElement>document.getElementById("comment")).value;
   	const token = localStorage.getItem("token")
	const encoded = btoa(token.toString()+(':k').toString())
	let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
        this.http.post(environment.commentServiceUrl + '/comments', {
        post_id: id,
        user_id: creator,
        content: comment
    }, { headers:headers}).subscribe(
      res => {
        console.log(res);
      },
      err => {
        console.log(err);
      }
    );
   }
 delete(id){
   	const token = localStorage.getItem("token")
	const encoded = btoa(token.toString()+(':k').toString())
	let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
        this.http.delete(environment.commentServiceUrl + '/comments/'+id, { headers:headers}).subscribe(
      res => {
        console.log(res);
      },
      err => {
        console.log(err);
      }
    );
   }

deletePost(id){
   	const token = localStorage.getItem("token")
	const encoded = btoa(token.toString()+(':k').toString())
	let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
        this.http.delete(environment.postServiceUrl + '/posts/'+id, { headers:headers}).subscribe(
      res => {
        console.log(res);
      },
      err => {
        console.log(err);
      }
    );
   }
}
