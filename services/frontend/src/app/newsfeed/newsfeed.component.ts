import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Navbar} from '../navbar';

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
  public likesLength : number
  public likesHolder :any;
  public likes = {};
  public adsHolder :any;
  public ads = [];
  public adsImage: string;
  public usersHolder :any
  public users = [];
  public usersObject = {};
  public cyberHolder :any
  public imageRoot = environment.adServiceUrl; 

  constructor(private http: HttpClient, public nav: Navbar) {
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
        const id = localStorage.getItem("id")
	const token = localStorage.getItem("token")
	const encoded = btoa(token.toString()+(':k').toString())
	let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);

        this.http.get(environment.newsfeedServiceUrl+'/newsfeed/'+id,{ headers:headers}).subscribe(
        res => {
        this.responseHolder = res;
	this.posts = this.responseHolder.data.posts;
        console.log(this.posts);
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

	this.http.get(environment.likeServiceUrl+'/likes/posts/'+post.id).subscribe(
        res => {
      	this.likesHolder = res;
	console.log(this.likesHolder);
	this.likes[post.id]=this.likesHolder.data.likes;
	});
	}
      },
      err => {
        console.log(err);
      });


      this.http.get(environment.adServiceUrl+'/ads/user/'+id,{ headers}).subscribe(
        res => {
        this.adsHolder = res;
	this.ads=this.adsHolder.data.ads;
        this.adsImage = this.ads[Math.floor(Math.random() * this.ads.length)].image
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
        this.cyberHolder = res["anti-cyberbullying"].result;
        console.log(this.cyberHolder);
        if(this.cyberHolder){
         const danger = (<HTMLInputElement>document.getElementById("danger"));
         danger.innerHTML="Your post did not pass the cyber bulling text";
        }
        const success = (<HTMLInputElement>document.getElementById("success"));
        success.innerHTML="Your post is submitted"
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
        const success = (<HTMLInputElement>document.getElementById("success"));
        success.innerHTML="Your like is submitted";
      },
      err => {
        console.log(err);
      }
    );	
}



comment(id){
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
        success.innerHTML="Your comment is submitted"
      },
      err => {
        console.log(err);
      }
    );
   }

}
