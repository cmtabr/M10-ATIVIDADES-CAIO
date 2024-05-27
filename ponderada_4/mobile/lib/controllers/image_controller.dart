import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import '../models/image.dart';

const String channelId = 'image_processing_channel';
const String channelName = 'Image Processing';
const String channelDescription = 'Status do processamento de imagem';

final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin = FlutterLocalNotificationsPlugin();

class ImageController {
  static Future<Uint8List?> sendImage(File image) async {
    final bytes = image.readAsBytesSync();
    final base64Image = base64Encode(bytes);
    final imageData = ImageData(base64Image: base64Image);

    try {
      final response = await http.post(
        Uri.parse('http://10.0.2.2:5002/remove-bg'),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(imageData.toJson()),
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> responseData = jsonDecode(response.body);
        final processedImage = ImageData.fromJson(responseData);
        await _showNotification('Image Processed', 'Your image has been successfully processed.');
        return base64Decode(processedImage.base64Image);
      } else {
        await _showNotification('Processing Failed', 'Não foi possível aplicar o filtro');
        return null;
      }
    } catch (e) {
      await _showNotification('Processing Failed', 'Não foi possível aplicar o filtro');
      return null;
    }
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
    await flutterLocalNotificationsPlugin.show(
      0,
      title,
      body,
      platformChannelSpecifics,
      payload: 'Tá bonitão hein',
    );
  }
}
