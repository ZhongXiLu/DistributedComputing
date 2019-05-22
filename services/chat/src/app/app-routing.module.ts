import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { SearchComponent } from './search/search.component';
import { ChatComponent } from './chat/chat.component';
import { Guard } from './guard';

const routes: Routes = 
[
  {
    path:'',
    component: LoginComponent
  },
  {
    path:'register',
    component: RegisterComponent
  },
  {
    path:'login',
    component: LoginComponent
  },
  {
    path:'chat',
    component: ChatComponent, canActivate:[Guard]
  },
  {
    path:'search',
    component: SearchComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
