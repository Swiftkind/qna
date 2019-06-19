import { ContentOnly } from '../../commons/utils/layout.utils';
import { IndexComponent } from './index/index.component';
import { SearchComponent } from './search/search.component';


export const PUBLIC_STATES : Object[] = [
  { name : 'index',
    url  : '/',
    views: ContentOnly(IndexComponent) 
  },
  { name : 'search',
    url  : '/search/',
    views: ContentOnly(SearchComponent) 
  }
]