import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import {FormsModule} from '@angular/forms'

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component"

import { HomeComponent } from './home/home.component';
import { AppareilComponent} from './appareil/appareil.component';
import { from } from 'rxjs';
import { BlogComponent } from './blog/blog.component';

@NgModule({
  declarations: [AppComponent, HomeComponent, AppareilComponent, BlogComponent],
  imports: [BrowserModule, AppRoutingModule, BrowserAnimationsModule,FormsModule],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
