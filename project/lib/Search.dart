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

class Search extends StatefulWidget {
  Search({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<Search> {
  Watson myWatson = new Watson();
  News news;
  List<Article> articles = [];
  List<Color> myColors;
  int page;
  int flag;
  String q;
  var Response;
  List<Color> C = [];
  MyDB mydb;
  TextEditingController _controller;
  final _formKey = GlobalKey<FormState>();

  // Init state. Check controller.
  void initState() {
    super.initState();
    mydb = MyDB();
    news = News();
    page = 0;
    flag = 0;
    _controller = TextEditingController();
  }

  // Works
  _launchURL(url) async {
    if (await canLaunch(url)) {
      await launch(url);
    } else {
      throw 'Could not launch $url';
    }
  }

  void Eureka() {
    Future.wait([news.getNews(q, 'en', 10)]).then((value) {
      getColor(value[0]).then((value) {
        setState(() {
          articles = value[1];
          myColors = value[0];
        });
      });
    });
  }

  Future<dynamic> getColor(List<Article> a) async {
    List<String> targets = q.split(" ");
    List<Color> temp = List.filled(a.length, Colors.blue);

    int i,j;
    var c,d,temp1;
    List<bool> aV = List.filled(a.length, true);
    List<String> comp = List.filled(targets.length + 1, '');

    for (i = 0; i < a.length; i++) {
      var myNiggaFlag = false;
      c = await myWatson.getResponse(a[i].url, targets);
      d = jsonDecode(c);
      if(i == 0){
        temp1 = d['sentiment']['targets'];
        for(j=0 ; j<temp1.length ; j++) {
          comp[j] = (temp1[j]['label']);
        }
        comp[comp.length - 1] = d['sentiment']['document']['label'];
        aV[0] = true;
      }
      else{
        temp1 = d['sentiment']['targets'];
        for(j=0 ; j<temp1.length ; j++) {
          if(comp[j] != temp1[j]['label']){
            aV[i] = false;
          }
        }
        if(comp[comp.length - 1] != d['sentiment']['document']['label']){
          aV[i] = false;
        }
      }

      if(aV[i]){
        temp[i] = Colors.blue;
      }
      else{
        temp[i] = Colors.yellow;
      }
    }

    return [temp, a];
  }

  listArticles() {
    if (articles == null) {
      return Center(
        child: Text('Nothing here. Search above'),
      );
    } else if (articles.length == 0) {
      return Center(
        child: Text('No articles :/'),
      );
    } else {
//      print('Im here');
      return ListView.builder(
          itemCount: articles.length,
          itemBuilder: (context, index) {
            return Dismissible(
                background: Container(color: Colors.blue[100]),
                onDismissed: (direction) {
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
                      trailing: Icon(
                        Icons.circle,
                        color: myColors[index],
                      ),
                      leading: IconButton(
                        highlightColor: Colors.blue,
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
                      ),
                      children: <Widget>[
                        Center(
                          child: Padding(
                            padding:
                                const EdgeInsets.fromLTRB(12.0, 12, 12, 0),
                            child: articles[index].urlToImage != null
                                ? Image.network(articles[index].urlToImage)
                                : Container(),
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
                  'News',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 40,
                  ),
                ),
                SizedBox(
                  width: 10,
                ),
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
                color: Colors.white),
            child: Padding(
                padding: EdgeInsets.fromLTRB(0, 15, 0, 0),
                child: Center(
                    child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Padding(
                      padding: const EdgeInsets.fromLTRB(20, 0, 20, 0),
                      child: Form(
                        key: _formKey,
                        child: Row(
                          children: <Widget>[
                            Expanded(
                              child: TextFormField(
                                keyboardType: TextInputType.text,
                                validator: (val) => val.length == 0
                                    ? "Enter a search term"
                                    : null,
                                onSaved: (String val) {
                                  setState(() {
                                    q = val;
                                    print(q);
                                    Eureka();
                                    setState(() {});
                                  });
                                },
                              ),
                            ),
                            IconButton(
                              onPressed: () {
                                // Validate returns true if the form is valid, otherwise false.
                                if (_formKey.currentState.validate()) {
                                  _formKey.currentState.save();
                                  Scaffold.of(context).showSnackBar(SnackBar(
                                      content: Text('Fetching articles')));
                                }
                              },
                              icon: Icon(Icons.search),
                            ),
                          ],
                        ),
                      ),
                    ),
                    Expanded(
                      child: Container(
                        child: listArticles(),
                      ),
                    )
                  ],
                ))),
            height: MediaQuery.of(context).size.height * 0.9,
          ),
        ),
      ],
    );
  }
}
