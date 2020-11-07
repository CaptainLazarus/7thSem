import 'package:flutter/material.dart';
import 'package:project/main.dart';
import 'package:provider/provider.dart';
import 'src/db.dart';
import 'package:url_launcher/url_launcher.dart';


class SaveData extends StatefulWidget {
  SaveData({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<SaveData> {

  MyDB mydb = MyDB();

  @override
  void initState() {
    super.initState();
  }

  _launchURL(url) async {
    if (await canLaunch(url)) {
      await launch(url);
    } else {
      throw 'Could not launch $url';
    }
  }

  ListView listBuilder(List<ArticleIndia> articles) {
//    print(articles.length);
    return ListView.builder(
        itemCount: articles.length,
        itemBuilder: (context , index) {
          return Dismissible(
            background: Container(color: Colors.red),
            onDismissed: (direction) {
              mydb.d(articles[index].id , articles[index]);
            },
            key: UniqueKey(),
            child: Center(
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: ExpansionTile(
                  key: PageStorageKey<String>(articles[index].title),
                  leading: IconButton(
                    icon: Icon(Icons.forward),
                    onPressed: () {
                      _launchURL(articles[index].url);
                    },
                  ),
                  title: Text(
                    articles[index].title,
//                    overflow: TextOverflow.ellipsis,
                  ),
                  children: <Widget>[
                    Center(
                      child: Padding(
                        padding: const EdgeInsets.fromLTRB(12.0 , 12 , 12 , 0),
                        child: articles[index].urlToImage != null ? Image.network(articles[index].urlToImage) : Container(),
                      ),
                    ),
//                    Center(
//                      child: Padding(
//                        padding: const EdgeInsets.all(12.0),
//                        child: RichText(
//                          text: TextSpan(
//                            text: articles[index].title,
//                            style: TextStyle(
//                                fontFamily: 'Garamond',
//                                fontSize: 16,
//                                color: Colors.black,
//                                fontWeight: FontWeight.bold
//                            ),
//                          ),
//                        ),
//                      ),
//                    ),
                    Center(
                      child: Padding(
                        padding: const EdgeInsets.all(12.0),
                        child: RichText(
                          text: TextSpan(
                            text: articles[index].content,
                            style: DefaultTextStyle.of(context).style,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            )
          );
        }
    );
  }


  list(x) {
    return FutureBuilder(
        future: x.items,
        builder: (context,snapshot) {
//          print(snapshot.data.length);
          if(snapshot.hasData) {
            if(snapshot.data.length == 0){
              return Center(child: Text("No Articles Found"));
            }
            return listBuilder(snapshot.data);
          }
          if(snapshot.data == null){
            return Text("DB not created");
          }
          return CircularProgressIndicator();
        }
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButton: FloatingActionButton(
        onPressed: (){
          setState(() {});
        },
        child: Icon(Icons.refresh),
      ),
      body: Center(
        child: Column(
          children: <Widget>[
            SizedBox(height: 20),
            Expanded(
              child: Consumer<MyDB>(
                builder: (context , mydb , child) {
                  return list(mydb);
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}