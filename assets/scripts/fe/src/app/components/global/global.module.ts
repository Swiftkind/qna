import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule as GlobalFormsModule } from './forms/forms.module';
import { FiltersModule as GlobalFiltersModule } from './filters/filters.module';

@NgModule({
  imports: [
    CommonModule,
    GlobalFormsModule,
    GlobalFiltersModule
  ],
  declarations: []
})
export class GlobalModule { }
