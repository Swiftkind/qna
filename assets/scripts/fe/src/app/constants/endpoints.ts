// export const API_DOMAIN = 'localhost:8000'

export const QUESTIONS_API_SEARCH = (page: string, keyword: string): string => '/api/questions/?page='+page+'&keyword='+keyword;
