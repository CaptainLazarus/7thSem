import 'package:flutter/material.dart';
import 'package:project/main.dart';
import 'package:provider/provider.dart';
import './db.dart';


class SaveData extends StatefulWidget {
  SaveData({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<SaveData> {

//  var cartModel = somehowGetMyCartModel(context);
//  Future<List<ArticleIndia>> items;

  MyDB mydb = MyDB();

  @override
  void initState() {
    super.initState();
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
                child: InkWell(
                  onTap: (){
                    print(articles[index].id.toString() + '\t' + index.toString());
                  },
                  child: Card(
                      child: Column(
                        mainAxisSize: MainAxisSize.max,
                        children: <Widget>[
                          ListTile(
                              title: Text(
                                  articles[index].title,
                                  overflow: TextOverflow.ellipsis,
                              ),
                          ),
                        ],
                      )
                  ),
                )
            ),
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
              return Text("No Articles Found");
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