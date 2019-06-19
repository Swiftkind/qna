import { Component, OnInit } from '@angular/core';
import { SearchService } from '../../../commons/services/search.service';

import { QUESTIONS_API_SEARCH } from '../../../constants/endpoints';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {

  questions$: any = {
    results: []
  };

  page = '1';

  constructor(
      private searchService: SearchService
  ) { }

  ngOnInit() {
      this.searchService.getQuestions(this.page)
      .subscribe(
          data => {
            this.questions$ = data;
          }
      );
  }

  counter(size) {
    return new Array(size);
  }

  goToPage(page){
    this.page = page;
    this.searchService.getQuestions(this.page)
    .subscribe(
        data => {
          this.questions$ = data;
        }
    );
  }

}
