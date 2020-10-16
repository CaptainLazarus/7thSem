import 'package:newsapi/newsapi.dart';

class News{
  NewsApi newsApi;

  News(){
    this.newsApi = NewsApi();
    this.newsApi.init(
      apiKey: '0a80713696c547b1a7bd11f0281e956f',
    );
  }

  Future<List<Article>> getNews(int pageNo) async {
    ArticleResponse response = await newsApi.everything(
      q: 'hathras',
      language: 'en',
//      pageSize: 100,
//      page: pageNo
    );

    return response.articles;
  }
}