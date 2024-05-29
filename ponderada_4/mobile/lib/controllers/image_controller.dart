import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import '../models/image.dart';

const String channelId = 'image_processing_channel';
const String channelName = 'Image Processing';
const String channelDescription = 'Status do processamento de imagem';

class ImageController {
  static final FlutterSecureStorage _storage = FlutterSecureStorage();
  static final FlutterLocalNotificationsPlugin _flutterLocalNotificationsPlugin =
      FlutterLocalNotificationsPlugin();
  
  static Future<Uint8List?> sendImage(File image) async {
    try {
      final bytes = await image.readAsBytes(); // Use async method to read bytes
      final base64Image = base64Encode(bytes);
      final imageData = ImageData(base64Image: base64Image);

      final authId = await _getAuthId();
      print('auth-id: $authId'); // Debugging line
      final response = await http.post(
        Uri.parse('http://10.0.2.2:3000/remove-bg'),
        headers: <String, String>{
          'Content-Type': 'application/json',
          'accept': 'application/json',
          'auth-id': '$authId', // Directly include authId as a string
        },
        body: jsonEncode(imageData.toJson()),
      );

      print('Response status: ${response.statusCode}'); // Debugging line
      print('Response body: ${response.body}'); // Debugging line

      if (response.statusCode == 200) {
        final Map<String, dynamic> responseData = jsonDecode(response.body);
        final processedImage = ImageData.fromJson(responseData);
        await _showNotification('Image Processed', 'Sua imagem foi processada com sucesso.');
        return base64Decode(processedImage.base64Image);
      } else {
        await _showNotification('Processing Failed', 'Não foi possível aplicar o filtro');
        return null;
      }
    } catch (e) {
      print('Exception: $e'); // Debugging line
      await _showNotification('Processing Failed', 'Não foi possível aplicar o filtro');
      return null;
    }
  }

  static Future<String?> _getAuthId() async {
    print(await _storage.read(key: 'auth_id'));
    return await _storage.read(key: 'auth_id');
  }

  static Future<void> _showNotification(String title, String body) async {
    const AndroidNotificationDetails androidPlatformChannelSpecifics =
        AndroidNotificationDetails(
      channelId,
      channelName,
      channelDescription: channelDescription,
      importance: Importance.max,
      priority: Priority.high,
      showWhen: false,
    );
    const NotificationDetails platformChannelSpecifics =
        NotificationDetails(android: androidPlatformChannelSpecifics);
    await _flutterLocalNotificationsPlugin.show(
      0,
      title,
      body,
      platformChannelSpecifics,
      payload: 'Bonito hein...',
    );
  }
}
