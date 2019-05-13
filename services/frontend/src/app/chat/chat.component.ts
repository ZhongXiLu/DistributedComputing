import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { TokenService } from '../login/token.service';
import { environment } from '../../environments/environment';
@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  welcome = "";
  public messageHolder : any;
  public messages = [];
  interval = 0;
  constructor(private http: HttpClient, private tokens: TokenService) {
    
   }

  ngOnInit() {
    	this.interval = setInterval(()=>{ 
	   this.retrieveMessages();
	},3000);
  }

 retrieveMessages(){
    	const creator = localStorage.getItem("id");
	const correspondent_id = 2
   	const token = localStorage.getItem("token")
	const encoded = btoa(token.toString()+(':k').toString())
	let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
        this.http.get(environment.messageServiceUrl + '/message/'+creator+'/'+1,{ headers:headers}).subscribe(
      res => {
        this.messageHolder = res;
	this.messages = this.messageHolder.messages;
        console.log(this.messages);
      },
      err => {
        console.log(err);
      }
    );
  }

 send(){
    	const creator = localStorage.getItem("id");
	const correspondent_id = 2;
	const message= (<HTMLInputElement>document.getElementById("message")).value;
   	const token = localStorage.getItem("token");
	const encoded = btoa(token.toString()+(':k').toString())
	let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
        this.http.post(environment.messageServiceUrl+'/message',
        { 
	contents:message,
	sender_id: creator,
	receiver_id: correspondent_id

	},{ headers:headers}).subscribe(
      res => {
        console.log(res);
      },
      err => {
        console.log(err);
      }
    );
  }


}
