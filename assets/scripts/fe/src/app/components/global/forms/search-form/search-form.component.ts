import { Component, OnInit } from '@angular/core';
import { StateService } from '@uirouter/angular';
import { NgForm } from '@angular/forms';
import { SearchService } from '../../../../commons/services/search.service';

@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.css']
})
export class SearchFormComponent implements OnInit {

  constructor(
      private stateService: StateService,
      private searchService: SearchService
  ) { }

  ngOnInit() {
  }

  search(searchForm: NgForm){
      console.log(searchForm.value)
      this.searchService.postQuestions('1',searchForm.value);
      this.stateService.go('search')
  }
}
