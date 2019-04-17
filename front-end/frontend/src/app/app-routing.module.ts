import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { ProfileComponent } from './profile/profile.component';
import { AdminComponent } from './admin/admin.component';
import { NewsfeedComponent } from './newsfeed/newsfeed.component';
import { ChatComponent } from './chat/chat.component';
const routes: Routes = 
[
  {
    path:'',
    component: HomeComponent
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
    path:'profile/:username',
    component: ProfileComponent
  },
  {
    path:'admin',
    component: AdminComponent
  },
  {
    path:'newsfeed/:username',
    component: NewsfeedComponent
  },
  {
    path:'chat/:username',
    component: ChatComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
