import { Component, OnInit } from '@angular/core';
import { SearchService } from '../../../commons/services/search.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {

  questions$: Object;

  constructor(
      private searchService: SearchService
  ) { }

  ngOnInit() {
      this.searchService.getQuestions().subscribe(
          searchService => this.questions$ = searchService
      );
  }

}
