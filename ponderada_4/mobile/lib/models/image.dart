class ImageData {
  final String base64Image;

  ImageData({required this.base64Image});

  Map<String, String> toJson() {
    return {
      'base64_image': base64Image,
    };
  }

  factory ImageData.fromJson(Map<String, dynamic> json) {
    return ImageData(
      base64Image: json['base64_image'],
    );
  }
}
