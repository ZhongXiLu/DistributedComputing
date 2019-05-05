import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-newsfeed',
  templateUrl: './newsfeed.component.html',
  styleUrls: ['./newsfeed.component.css']
})
export class NewsfeedComponent implements OnInit {

  constructor(private http: HttpClient) {
   }

  ngOnInit() {
    
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
