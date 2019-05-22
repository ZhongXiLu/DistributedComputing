// admin.ts

import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { Observable } from 'rxjs';

@Injectable()
export class Admin implements CanActivate {

  constructor(private router: Router) {}

  canActivate(): Observable<boolean> | Promise<boolean> | boolean {
    const token = localStorage.getItem("token")
    const admin= localStorage.getItem("admin")
    if(admin=="true"){  
	return true;
    }
    else{
	this.router.navigate(['/login']);
    }
    


  }
}
