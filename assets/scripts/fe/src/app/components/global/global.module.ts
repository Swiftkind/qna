import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule as GlobalFormsModule } from './forms/forms.module';

@NgModule({
  imports: [
    CommonModule,
    GlobalFormsModule
  ],
  declarations: []
})
export class GlobalModule { }
