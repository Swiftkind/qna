import { FePage } from './app.po';

describe('fe App', function() {
  let page: FePage;

  beforeEach(() => {
    page = new FePage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
