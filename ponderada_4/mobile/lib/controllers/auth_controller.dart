import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import '../models/user.dart';

class AuthController {
  static const FlutterSecureStorage _storage = FlutterSecureStorage();

  static Future<void> login(User user, BuildContext context) async {
    final response = await http.post(
      Uri.parse('http://10.0.2.2:3000/user/login'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(user.toJson()),
    );

    if (response.statusCode == 200) {
      final responseData = jsonDecode(response.body);
      final String authId = responseData['auth_id'];
      await _storeAuthId(authId);
      Navigator.pushReplacementNamed(context, '/home');
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Falha no login')),
      );
    }
  }

  static Future<void> _storeAuthId(String authId) async {
    await _storage.write(key: 'auth_id', value: authId);
  }

  static Future<String?> getAuthId() async {
    return await _storage.read(key: 'auth_id');
  }

  static Future<void> logout(BuildContext context) async {
    await _storage.delete(key: 'auth_id');
    Navigator.pushReplacementNamed(context, '/login');
  }

  static Future<void> signup(User user, BuildContext context) async {
    final response = await http.post(
      Uri.parse('http://10.0.2.2:3000/user/signup'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(user.toJson()),
    );

    if (response.statusCode == 200) {
      Navigator.pushReplacementNamed(context, '/');
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Falha no cadastro')),
      );
    }
  }
}
