import 'package:flutter/foundation.dart';

import 'db.dart';
import 'dart:async';
import 'dart:io' as io;
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path_provider/path_provider.dart';

class DBHelper{
  static Database _db;
  static const String TABLE = 'articles';
  static const String id = 'id';
  static const String title = 'title';
  static const String content = 'content';
  static const String source = 'source';
  static const String url = 'url';
  static const String urlToImage = 'urlToImage';
  static const DB_NAME = 'subjects.db';

  Future<Database> get db async {
    if(_db != null) {
      return _db;
    }
    _db = await initDB();
    return _db;
  }

  initDB() async {
    io.Directory directory = await getApplicationDocumentsDirectory();
    String path = join(directory.path , DB_NAME);
    var db = await openDatabase(path , version: 1 , onCreate: _onCreate);
    return db;
  }

  _onCreate(Database db , int version) async {
    await db.execute("CREATE TABLE  $TABLE ($id INTEGER PRIMARY KEY , $title TEXT , $content TEXT , $source TEXT , $url TEXT , $urlToImage TEXT)");
  }

  Future<ArticleIndia> save(ArticleIndia article) async {
    var database = await db;
    article.id = await database.insert(TABLE, article.toMap());
    return article;
  }

  Future<List<ArticleIndia>> getArticles() async {
    var database = await db;
    List<Map> maps = await database.query(TABLE , columns:[id,title,content,source,url,urlToImage]);
    List<ArticleIndia> articles = [];
    if(maps.length > 0){
      for(int i=0 ; i<maps.length ; i++){
        articles.add(ArticleIndia.fromMap(maps[i]));
        print(articles[i].id);
      }
    }
    
    return articles;
  }

  Future<int> delete(int i) async {
    var database = await db;
    var a = await database.delete(TABLE , where:'$id = ?' , whereArgs: [i]);
    return a;
  }

//  Future<int> update(ArticleIndia article) async {
//    var database = await db;
//    return await database.update(TABLE, article.toMap() , where: "$id = ?" , whereArgs: [article.id]);
//  }

  Future close() async {
    var database = await db;
    database.close();
  }
}