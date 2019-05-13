import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-newsfeed',
  templateUrl: './newsfeed.component.html',
  styleUrls: ['./newsfeed.component.css']
})
export class NewsfeedComponent implements OnInit {
  public responseHolder :any;
  public dataHolder :any;
  public posts = [];
  public commentHolder :any;
  public comments = {};
  public tagsHolder :any;
  public tags = {};
  constructor(private http: HttpClient) {
   }

  ngOnInit() { 
        const id = localStorage.getItem("id")
	const token = localStorage.getItem("token")
	const encoded = btoa(token.toString()+(':k').toString())
	let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);

        this.http.get(environment.newsfeedServiceUrl+'/newsfeed/'+id,{ headers:headers}).subscribe(
        res => {
        this.responseHolder = res;
	this.posts = this.responseHolder.data.posts;
      for (let post of this.posts){
	this.http.get(environment.commentServiceUrl+'/comments/posts/'+post.id).subscribe(
        res => {
      	this.commentHolder = res;
	console.log(this.commentHolder);
	this.comments[post.id]=this.commentHolder.data.comments;
	});
	
	this.http.get(environment.tagServiceUrl+'/tags/posts/'+post.id).subscribe(
        res => {
      	this.tagsHolder = res;
	console.log(this.tagsHolder);
	this.tags[post.id]=this.tagsHolder.data.tags;
	}); 
	}
      },
      err => {
        console.log(err);
      });


      this.http.get(environment.adServiceUrl+'/ads/user/'+id,{ headers}).subscribe(
        res => {
        console.log(res)
      },
      err => {
        console.log(err);
      });
    
  }

   submit(event) {
	event.preventDefault();
	const token = localStorage.getItem("token")
	const encoded = btoa(token.toString()+(':k').toString())
    	const message = (<HTMLInputElement>document.getElementById("message")).value;
	const tags = (<HTMLInputElement>document.getElementById("tags")).value;
	const tagsArray = tags.split(",");
    	const creator = localStorage.getItem("id")
   	let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
        this.http.post(environment.postServiceUrl + '/posts', {
        content: message,
        creator: creator,
        tags: tagsArray
    }, { headers:headers}).subscribe(
      res => {
        console.log(res);
      },
      err => {
        console.log(err);
      }
    );
  }

  like(id){
    	const user_id = localStorage.getItem("id")
   	const token = localStorage.getItem("token")
	const encoded = btoa(token.toString()+(':k').toString())
	let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
        this.http.post(environment.likeServiceUrl + '/likes', {
        post_id: id,
        user_id: user_id
    }, { headers:headers}).subscribe(
      res => {
        console.log(res);
      },
      err => {
        console.log(err);
      }
    );	
}

comment(id){
    	const creator = localStorage.getItem("id");
	const comment= (<HTMLInputElement>document.getElementById("comment")).value;
   	const token = localStorage.getItem("token")
	const encoded = btoa(token.toString()+(':k').toString())
	let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
        this.http.post(environment.commentServiceUrl + '/comments', {
        post_id: 1,
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

}
