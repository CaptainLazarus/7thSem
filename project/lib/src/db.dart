class ArticleIndia{
  int id;
  String title;
  String content;
  String source;
  String url;
  String urlToImage;


  ArticleIndia(article) {
    this.title = article.title;
    this.content = article.content;
    this.source = article.source.name;
    this.url = article.url;
    this.urlToImage = article.urlToImage;
//    this.id = id;
  }

  Map<String, dynamic> toMap() {
    var map = <String , dynamic>{
      'id': id,
      'title': title,
      'content': content,
      'source': source,
      'url': url,
      'urlToImage': urlToImage
    };
    return map;
  }

  ArticleIndia.fromMap(Map<String , dynamic> map) {
    id = map['id'];
    title = map['title'];
    content = map["content"];
    source = map["source"];
    url = map["url"];
    urlToImage = map["urlToImage"];
  }

  @override
  String toString() {
    return 'ArticleIndia{id: $id, title: $title, content: $content, source: $source, url: $url, urlToImage: $urlToImage}';
  }
}