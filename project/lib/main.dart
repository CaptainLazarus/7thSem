import 'dart:ffi';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:project/src/db.dart';
import 'package:project/src/db_func.dart';
import 'src/Home.dart';
import 'src/Saved.dart';
import 'package:provider/provider.dart';
import 'src/db_func.dart';

void main() async{
  runApp(
    MultiProvider(
        providers: [
          ChangeNotifierProvider(
            create: (context) => MyDB(),
          ),
        ],
        child: MyApp()),
  );
}

class MyDB extends ChangeNotifier{
  DBHelper _dbHelper = DBHelper();
//  List<ArticleIndia> _items = [];

  get items => _dbHelper.getArticles().then((value) => value);
  
  s(ArticleIndia a) {
    _dbHelper.save(a).then((value) {
      notifyListeners();
    });
  }

  d(int i , ArticleIndia a) {
    _dbHelper.delete(i).then((value) {
      notifyListeners();
    });
  }
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        fontFamily: 'Garamond',
        primarySwatch: Colors.lightGreen,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      routes: {
        '/': (context) => MyHomePage(title: 'Yeah',),
        '/a': (context) => SaveData(),
      },
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {

  int _selectedIndex = 0;
  final PageStorageBucket bucket = PageStorageBucket();


  final List<Widget> pages = [
    Home(
      key: PageStorageKey('Home'),
    ),
    SaveData(
      key: PageStorageKey('Saved'),
    ),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }


  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        backgroundColor: Colors.black,
        body: IndexedStack(
          index: _selectedIndex,
          children: pages,
        ),
        bottomNavigationBar: BottomNavigationBar(
          items: const <BottomNavigationBarItem>[
            BottomNavigationBarItem(
                icon: Icon(Icons.home),
                title: Text('Home')
            ),
            BottomNavigationBarItem(
                icon: Icon(Icons.save_alt),
                title: Text('Saved')
            )
          ],
          currentIndex: _selectedIndex,
          selectedItemColor: Colors.amber[800],
          onTap: _onItemTapped,
        ),
      ),
    );
  }
}
