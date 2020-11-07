import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:project/main.dart';
import 'package:project/src/db.dart';
import 'package:project/src/news.dart';
import 'package:newsapi/newsapi.dart';
import 'package:project/src/watson.dart';
import 'package:url_launcher/url_launcher.dart';
import 'src/watson.dart';

class Home extends StatefulWidget {
  const Home({Key key}) : super(key: key);

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<Home> {

  Watson myWatson = new Watson();
  News news;
  Future<List<Article>> articles;
  int page;
  int flag;
  var Response;
  MyDB mydb;

  void initState() {
    super.initState();
    mydb = MyDB();
    news = News();
    page = 0;
    flag = 0;
    refreshNews(page);
  }


  _launchURL(url) async {
    if (await canLaunch(url)) {
      await launch(url);
    } else {
      throw 'Could not launch $url';
    }
  }

  refreshNews(int x) {
    setState(() {
      articles = news.getNews('India' , 'en', 20);
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
                child: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: ExpansionTile(
                    key: PageStorageKey<String>(articles[index].title),
                    leading: IconButton(
                      color: Colors.black,
                      key: UniqueKey(),
                      icon: Icon(
                        Icons.save_alt,
                      ),

                      onPressed: () {
                        mydb.s(ArticleIndia(articles[index]));
                      },
                    ),
                    title: Text(
                      articles[index].title,
                    ),
                    children: <Widget>[
                      Center(
                        child: Padding(
                          padding: const EdgeInsets.fromLTRB(12.0 , 12 , 12 , 0),
                          child: articles[index].urlToImage != null ? Image.network(articles[index].urlToImage) : Container(),
                        ),
                      ),
                      Center(
                        child: Padding(
                          padding: const EdgeInsets.all(12.0),
                          child: RichText(
                            text: TextSpan(
                              text: articles[index].description,
                              style: DefaultTextStyle.of(context).style,
                            ),
                          ),
                        ),
                      ),
                      ButtonBar(
                        alignment: MainAxisAlignment.spaceAround,
                        children: [
                          RaisedButton(
                            child: Text('Analyse'),
                            onPressed: () {
//                                myWatson.getResponse(articles[index].url).then((value) {
//                                  setState(() {
//                                    Response = jsonDecode(value);
//                                    String key = Response['keywords'][0]['text'];
//                                    for(var i=1 ; i<Response['keywords'].length ; i+=1){
//                                      key = key + ' AND ' + Response['keywords'][i]['text'];
//                                      print(Response['keywords'][i]);
//                                    }
//                                  });
//                                });
                              },
                          ),
                          IconButton(
                            icon: Icon(Icons.forward),
                            onPressed: () {
                              _launchURL(articles[index].url);
                            },
                          )
                        ],
                      )
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
              return Center(child: Text("No articles Found"));
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
