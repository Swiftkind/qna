import { ContentOnly } from '../../commons/utils/layout.utils';
import { IndexComponent } from './index/index.component';


export const PUBLIC_STATES : Object[] = [
  { name : 'index',
    url  : '/',
    views: ContentOnly(IndexComponent) 
  }
]