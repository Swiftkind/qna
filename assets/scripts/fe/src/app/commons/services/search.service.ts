import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  constructor(
      private http: HttpClient
  ) { }
  
  data;

  getQuestions(){
      return this.data;
  }

  postQuestions(page, data){
      this.data = this.http.post('/api/questions/search/?page='+page, data);
      console.log(this.data);
  }

}
