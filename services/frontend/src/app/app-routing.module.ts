import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { ProfileComponent } from './profile/profile.component';
import { AdminComponent } from './admin/admin.component';
import { SearchComponent } from './search/search.component';
import { NewsfeedComponent } from './newsfeed/newsfeed.component';
import { ChatComponent } from './chat/chat.component';
import { Guard } from './guard';
import { Admin } from './admin';

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
    path:'profile/:username',
    component: ProfileComponent, canActivate:[Guard]
  },
  {
    path:'admin',
    component: AdminComponent, canActivate:[Admin]
  },
  {
    path:'newsfeed',
    component: NewsfeedComponent, canActivate:[Guard]
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
