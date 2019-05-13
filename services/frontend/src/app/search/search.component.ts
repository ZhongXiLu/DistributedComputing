import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';

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
  constructor(private http: HttpClient) { 
    this.http.get(environment.userServiceUrl+'/users').subscribe(
      res => {
        this.responseHolder = res;
	this.users = this.responseHolder.data.users;
	console.log(this.users);
      },
      err => {
        console.log("Error occured");
      }
    );
  }

  ngOnInit() {

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
    	const follower = localStorage.getItem("id")
   	let headers: HttpHeaders = new HttpHeaders();
    	headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    	headers.append('Authorization', localStorage.getItem("token"));
        this.http.post(environment.followServiceUrl + '/follow', {
        follower_id: follower,
        followee_id: id
    }, { headers}).subscribe(
      res => {
        console.log(res);
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

        this.http.put(environment.friendServiceUrl + '/friend/request', {
        friend_initiator_id: id,
        friend_acceptor_id: friend_acceptor_id
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
    	const friend_2 = localStorage.getItem("id")
    	const token = localStorage.getItem("token")
	const encoded = btoa(token.toString()+(':k').toString())
	let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
        this.http.delete(environment.friendServiceUrl + '/friend/'+id+'/'+friend_2, { headers:headers}).subscribe(
      res => {
        console.log(res);
      },
      err => {
        console.log(err);
      }
    );
   }

}
