import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { TokenService } from '../login/token.service';
import { environment } from '../../environments/environment';
import { Navbar} from '../navbar';
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
  public usersHolder :any
  public cyberHolder :any
  public users = [];
  public usersObject = {};
  public friend = localStorage.getItem("friend");
  constructor(private http: HttpClient, private tokens: TokenService,public nav: Navbar) {
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
    	this.interval = setInterval(()=>{ 
	   this.retrieveMessages();
	},3000);
  }

 retrieveMessages(){
    	const creator = localStorage.getItem("id");
	const correspondent_id = localStorage.getItem("friend");
   	const token = localStorage.getItem("token")
	const encoded = btoa(token.toString()+(':k').toString())
	let headers: HttpHeaders = new HttpHeaders().set('content-type','application/json').set('Authorization', 'Basic '+encoded);
        this.http.get(environment.messageServiceUrl + '/message/'+creator+'/'+correspondent_id,{ headers:headers}).subscribe(
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
	const correspondent_id = localStorage.getItem("friend");
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
        this.cyberHolder = res["anti-cyberbullying"].result;
        console.log(this.cyberHolder);
        if(this.cyberHolder){
         const danger = (<HTMLInputElement>document.getElementById("danger"));
         danger.innerHTML="Your text did not pass the cyber bulling text";
        }
        
      },
      err => {
        console.log(err);
      }
    );
  }


}
