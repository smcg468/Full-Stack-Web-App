import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { WebService } from './web.service';
import { HttpClientModule } from '@angular/common/http';
import { OfficeEpisodesComponent } from './officeEpisodes/officeEpisodes.component';
import { RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { OfficeEpisodeComponent } from './officeEpisode/officeEpisode.component';
import { ReactiveFormsModule } from '@angular/forms';
import { NavbarComponent } from './navbar/navbar.component';
import { EpisodeReviewsComponent } from './reviews/episode_reviews.component';
import { AuthModule } from '@auth0/auth0-angular';
import {environment as env } from '../environments/environment'
import { LoginComponent } from './users/login.component'
import { LogoutComponent } from './users/logout.component';
import { UserProfileComponent } from './userProfile/userProfile.component';
import { AuthGuard } from '@auth0/auth0-angular';
import { Review_PostComponent } from './reviews/review_post.component';
import { FooterComponent } from './footer/footer.component';
import { OfficeSeasonsComponent } from './officeEpisodes/officeSeasons.component';
//import { RegisterComponent } from './users/register.component';
//import { AuthService } from './auth.service';


var routes: any = [
  {
    path: '',
    component: HomeComponent
  },
  {
    path: 'officeEpisodes',
    component: OfficeEpisodesComponent
  },
  {
    path: "seasons",
    component: OfficeSeasonsComponent
  },
  {
    path: 'officeEpisode/:id',
    component: OfficeEpisodeComponent
  },
  {
    path: 'userProfile',
    component: UserProfileComponent,
    canActivate: [AuthGuard]
  },
  {
    path: "login",
    component: LoginComponent
  }
];

@NgModule({
  declarations: [
    AppComponent, OfficeEpisodesComponent, HomeComponent, OfficeEpisodeComponent, NavbarComponent, EpisodeReviewsComponent,
    LoginComponent, LogoutComponent, UserProfileComponent, Review_PostComponent, FooterComponent,
     OfficeSeasonsComponent
  ],
  imports: [
    BrowserModule, HttpClientModule,
    RouterModule.forRoot(routes), ReactiveFormsModule,
    AuthModule.forRoot({
      domain: 'dev-gsxjpwqs.us.auth0.com',
      clientId:'Kws4fGi9VvLFcBuR8jSYs2Guw3xmEvni'
    })
  ],
  providers: [WebService],
  bootstrap: [AppComponent]
})
export class AppModule { }
