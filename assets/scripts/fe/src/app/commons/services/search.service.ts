import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { QUESTIONS_API_SEARCH } from '../../constants/endpoints';


@Injectable({
  providedIn: 'root'
})
export class SearchService {

  constructor(
      private http: HttpClient
  ) { }
  
  data = '';

  getQuestions(page){
      return this.http.get(QUESTIONS_API_SEARCH(page, this.data));
  }

  searchQuestions(data: string){ 
      this.data = data;
  }

}
