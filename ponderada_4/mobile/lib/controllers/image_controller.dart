import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import '../models/image.dart';

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
        return base64Decode(processedImage.base64Image);
      } else {
        print('Upload failed!');
        return null;
      }
    } catch (e) {
      print('Error: $e');
      return null;
    }
  }
}
