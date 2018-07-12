
export class QuestionURL{
    public static get API_QUESTION_URL():string {
        return '/questions/';
    }
    public static API_DETAILS_URL(code:string):string {
        return '/questions/'+code;
    }
}
