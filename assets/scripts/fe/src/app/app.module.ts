import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';

import { UIRouterModule } from '@uirouter/angular';

import { APP_STATES } from './commons/states/app.states';

import { PublicModule } from './components/public/public.module';
import { AppComponent } from './app.component';
import { GlobalModule } from './components/global/global.module';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    UIRouterModule.forRoot(APP_STATES),
    PublicModule,
    HttpClientModule,
    GlobalModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
