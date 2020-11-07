import 'package:newsapi/newsapi.dart';

class News{
  NewsApi newsApi;

  News(){
    this.newsApi = NewsApi();
    this.newsApi.init(
      apiKey: '0a80713696c547b1a7bd11f0281e956f',
    );
  }

  Future<List<Article>> getNews(String Q , String lang , int pageSize) async {
    ArticleResponse response = await newsApi.everything(
      q: Q,
      language: lang,
      sources: "fox-news , cnn" ,
      pageSize: pageSize
    );

    return response.articles;
  }

  Future<List<Article>> getHeadlines(String count , String lang , int pSize) async {
    ArticleResponse response = await newsApi.topHeadlines(
//      category: 'general',
      country: 'in',
      language: lang,
      pageSize: pSize,
    );

    return response.articles;
  }

}