import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';
import { Navbar} from '../navbar';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  public responseHolder :any
  public users = [];
  public friendsHolder :any
  public friends = [];
  public requestsHolder :any
  public requests = [];
  public usersObject = {};
  constructor(private http: HttpClient, private router:Router,public nav: Navbar) { 
    this.http.get(environment.userServiceUrl+'/users').subscribe(
      res => {
        this.responseHolder = res;
	this.users = this.responseHolder.data.users;
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
    const user = localStorage.getItem("id")

    this.http.get(environment.friendServiceUrl+'/friend/'+user+'/requests').subscribe(
      res => {
        this.requestsHolder = res;
	this.requests = this.requestsHolder.friends_requests;
	console.log(this.requests);
      },
      err => {
        console.log(err);
      }
    );

    this.http.get(environment.friendServiceUrl+'/friend/'+user).subscribe(
      res => {
        this.friendsHolder = res;
	this.friends = this.friendsHolder.friends;
	console.log(this.friends);
      },
      err => {
        console.log(err);
      }
    );
    
  }

 follow(id){
    	const follower = localStorage.getItem("id");
   	const token = localStorage.getItem("token");
	const encoded = btoa(token.toString()+(':k').toString());
	let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
        this.http.post(environment.followServiceUrl + '/follow', {
        follower_id: follower,
        followee_id: id
    }, { headers:headers}).subscribe(
      res => {
        console.log(res);
        const success = (<HTMLInputElement>document.getElementById("success"));
        success.innerHTML="Followed"
      },
      err => {
        console.log(err);
      }
    );
   }

beFriend(id){
    	const friend_initiator_id = localStorage.getItem("id")
    	const token = localStorage.getItem("token")
	const encoded = btoa(token.toString()+(':k').toString())
	let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
        this.http.post(environment.friendServiceUrl + '/friend/request', {
        friend_initiator_id: friend_initiator_id,
        friend_acceptor_id: id
    }, { headers:headers}).subscribe(
      res => {
        console.log(res);
	const success = (<HTMLInputElement>document.getElementById("success"));
        success.innerHTML="Befriended"
      },
      err => {
        console.log(err);
      }
    );
   }

accept(id){
    	const friend_acceptor_id = localStorage.getItem("id")
    	const token = localStorage.getItem("token")
	const encoded = btoa(token.toString()+(':k').toString())
	let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);

        this.http.put(environment.friendServiceUrl + '/friend/accept', {
        friend_initiator_id: id,
        friend_acceptor_id: friend_acceptor_id
    }, { headers:headers}).subscribe(
      res => {
        console.log(res);
	const success = (<HTMLInputElement>document.getElementById("success"));
        success.innerHTML="Request accepted"
      },
      err => {
        console.log(err);
      }
    );
   }

delete(id){
    	const friend_2 = localStorage.getItem("id")
    	const token = localStorage.getItem("token")
	const encoded = btoa(token.toString()+(':k').toString())
	let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
        this.http.delete(environment.friendServiceUrl + '/friend/'+id+'/'+friend_2, { headers:headers}).subscribe(
      res => {
        console.log(res);
	const success = (<HTMLInputElement>document.getElementById("success"));
        success.innerHTML="Friendship deleted"
      },
      err => {
        console.log(err);
      }
    );
   }

setConversation(friend){
	localStorage.setItem('friend', friend);
	this.router.navigate(['/chat']);
   }

}
