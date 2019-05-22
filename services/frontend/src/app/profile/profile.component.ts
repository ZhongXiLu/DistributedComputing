import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Navbar} from '../navbar';

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
  public usersHolder :any
  public users = [];
  public usersObject = {};
  public tagsHolder :any;
  public tags = {};
  public likesLength : number
  public likesHolder :any;
  public likes = {};
  constructor(private http: HttpClient, public nav: Navbar) 
   {
      this.http.get(environment.userServiceUrl+'/users').subscribe(
      res => {
        this.usersHolder = res;
	this.users = this.usersHolder.data.users;
	console.log(this.users);
        for (let obj of this.users){
           this.usersObject[obj.id]=obj.username;
        }
      },
      err => {
        console.log("Error occured");
      }
    );
   }

  ngOnInit() { 
        this.nav.show();
        const id = localStorage.getItem('id');
	console.log(id);
	this.http.get(environment.userServiceUrl+'/users/'+id).subscribe(
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
        this.http.get(environment.tagServiceUrl+'/tags/posts/'+post.id).subscribe(
        res => {
      	this.tagsHolder = res;
	console.log(this.tagsHolder);
	this.tags[post.id]=this.tagsHolder.data.tags;
	}); 

	this.http.get(environment.likeServiceUrl+'/likes/posts/'+post.id).subscribe(
        res => {
      	this.likesHolder = res;
	console.log(this.likesHolder);
	this.likes[post.id]=this.likesHolder.data.likes;
        this.likesLength = this.likesHolder.data.likes.length;
	}); 
	}
      },
      err => {
        console.log(err);
      });
 
  }

   submitComment(id){
    	const creator = localStorage.getItem("id");
	const comment= (<HTMLInputElement>document.getElementById(id)).value;
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
        const success = (<HTMLInputElement>document.getElementById("success"));
        success.innerHTML="Comment added"
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
        const success = (<HTMLInputElement>document.getElementById("success"));
        success.innerHTML="Comment deleted"
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
	const success = (<HTMLInputElement>document.getElementById("success"));
        success.innerHTML="Post deleted"
      },
      err => {
        console.log(err);
      }
    );
   }
}
