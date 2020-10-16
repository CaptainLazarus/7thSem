import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:project/main.dart';
import 'package:project/src/db.dart';
import 'package:project/src/db_func.dart';
import 'package:project/src/news.dart';
import 'package:newsapi/newsapi.dart';

class Home extends StatefulWidget {
  const Home({Key key}) : super(key: key);

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<Home> {
  News news;
  Future<List<Article>> articles;
  int page;
  int flag;

  MyDB mydb;

  void initState() {
    super.initState();
    mydb = MyDB();
    news = News();
    page = 0;
    flag = 0;
    refreshNews(page);
  }

  refreshNews(int x) {
    setState(() {
      articles = news.getNews(x);
    });
  }

  ListView listBuilder(List<Article> articles) {
    return ListView.builder(
        itemCount: articles.length,
        itemBuilder: (context, index) {
          return Dismissible(
              background: Container(color: Colors.blue[100]),
              onDismissed: (direction) {
//              var id = UniqueKey();
                setState(() {
                  articles.removeAt(index);
                });
              },
              key: UniqueKey(),
              child: Center(
                child: Card(
                  child: Column(
                    children: <Widget>[
                      ListTile(
                        leading: IconButton(
                          highlightColor: Colors.red,
                            icon: Icon(
                              Icons.save_alt,
                              color: Colors.black,
                            ),
                            onPressed: () {
                                mydb.s(ArticleIndia(articles[index]));
                            },
                        ),
                        title: Text(
                          articles[index].title,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                      Center(
                        child: Padding(
                          padding: const EdgeInsets.all(8.0),
                          child: RichText(
                            maxLines: 2,
                            text: TextSpan(
                              text: articles[index].description,
                              style: DefaultTextStyle.of(context).style,
                            ),
                            overflow: TextOverflow.fade,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ));
        });
  }

  listArticles() {
    return FutureBuilder(
        future: articles,
        builder: (context, snapshot) {
//          print(snapshot.data);
          if (snapshot.hasData) {
            if (snapshot.data.length == 0) {
              return Text("No articles Found");
            }
            return listBuilder(snapshot.data);
          }
          return Center(child: CircularProgressIndicator());
        });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.end,
      children: <Widget>[
        Container(
          height: 100,
          child: Center(
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Text(
                  'News' ,
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 40,
                  ),
                ),
                SizedBox(width: 10,),
                Icon(
                  Icons.wifi,
                  color: Colors.white,
                  size: 40,
                )
              ],
            ),
          ),
        ),
        Expanded(
          child: Container(
//            margin: EdgeInsets.fromLTRB(0, 20, 0 , 0),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(15),
                topRight: Radius.circular(15),
              ),
              color: Colors.white
            ),
            child: Padding(
              padding: EdgeInsets.fromLTRB(0, 15 , 0 , 0),
              child: listArticles()
            ),
            height: MediaQuery.of(context).size.height * 0.9,
          ),
        ),
      ],
    );
  }
}
