import 'dart:ffi';
import 'dart:io';
import 'dart:convert';
import 'package:http/http.dart' as http;

class Watson {

  String apiKey = 'WB3mJb6FMOhv-JZXkJ9wD1admOJcmXeyy5wvxt0bZUvI';
  String url = "https://api.jp-tok.natural-language-understanding.watson.cloud.ibm.com/instances/974c600d-8bf1-4a35-9c2f-777bb37a0bb3/v1/analyze?version=2019-07-12";

  Future<dynamic> getResponse(String URL) async{
    String basicAuth = 'Basic ' + base64Encode(utf8.encode('apikey:'+apiKey));

    Map<String, String> requestHeaders = {
      "Content-Type": "application/json",
      'authorization': basicAuth
    };

    String _body = '''{
        "url": \"$URL\",
        "features": {
          "entities": {
            "sentiment": true,
            "limit": 4
          }
        }
    }''';

    var response = await http.post(
        this.url ,
        headers: requestHeaders,
        body: _body
    );

    var decoded = response.body;
    return decoded;
  }

}