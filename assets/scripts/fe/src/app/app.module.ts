import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { UIRouterModule } from '@uirouter/angular';

import { APP_STATES } from './commons/states/app.states';

import { PublicModule } from './components/public/public.module';
import { AppComponent } from './app.component';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    UIRouterModule.forRoot(APP_STATES),
    PublicModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
