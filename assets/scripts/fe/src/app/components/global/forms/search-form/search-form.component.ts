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
      if (searchForm.value.keyword != '') {
        this.searchService.searchQuestions(searchForm.value.keyword);

        this.stateService.go('search');
        if(this.stateService.$current.url.pattern == '/search/'){
          this.stateService.reload();
        }
      }
  }
}
