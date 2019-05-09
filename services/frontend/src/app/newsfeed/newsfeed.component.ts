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
  constructor(private http: HttpClient) {
   }

  ngOnInit() { 
        const id = localStorage.getItem("id")
	let headers: HttpHeaders = new HttpHeaders();
    	headers.append('Content-Type', 'application/x-www-form-urlencoded;   charset=UTF-8');
    	headers.append('Authorization', localStorage.getItem("token"));
        this.http.get(environment.newsfeedServiceUrl+'/newsfeed/'+id,{ headers}).subscribe(
        res => {
        console.log(res);
      },
      err => {
        console.log(err);
      });
    
  }

   submit(event) {
	event.preventDefault();
    	const message = (<HTMLInputElement>document.getElementById("message")).value;
    	const creator = localStorage.getItem("id")
   	let headers: HttpHeaders = new HttpHeaders();
    	headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    	headers.append('Authorization', localStorage.getItem("token"));
        this.http.post(environment.postServiceUrl + '/posts', {
        content: message,
        creator: creator,
        tags: [1,2]
    }, { headers}).subscribe(
      res => {
        console.log(res);
      },
      err => {
        console.log(err);
      }
    );
  }

}
