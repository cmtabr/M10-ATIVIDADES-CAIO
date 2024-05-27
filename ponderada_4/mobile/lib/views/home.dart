import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../controllers/image_controller.dart';

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  MyHomePageState createState() => MyHomePageState();
}

class MyHomePageState extends State<MyHomePage> {
  File? _image;
  Uint8List? _processedImage;
  final ImagePicker _picker = ImagePicker();

  Future<void> _pickImage() async {
    final pickedFile = await _picker.pickImage(source: ImageSource.gallery);

    setState(() {
      if (pickedFile != null) {
        _image = File(pickedFile.path);
        _processedImage = null;
      } else {
        print('Nenhuma imagem selecionada.');
      }
    });
  }

  Future<void> _sendImage() async {
    if (_image == null) return;

    _showLoadingDialog();
    final processedImage = await ImageController.sendImage(_image!);
    Navigator.of(context).pop();

    setState(() {
      _processedImage = processedImage;
      _image = null;
    });

    if (_processedImage != null) {
      _showProcessedImageDialog();
    } else {
      print('Falha ao processar a imagem.');
    }
  }

  void _showLoadingDialog() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return AlertDialog(
          content: Container(
            width: 20,
            height: 20,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(6),
              color: Colors.blue,
            ),
            child: const Center(
              child: CircularProgressIndicator(
                valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
              ),
            ),
          ),
        );
      },
    );
  }

  void _showProcessedImageDialog() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          content: _processedImage == null
              ? const Text('Sem imagem processada.')
              : Image.memory(_processedImage!),
          actions: <Widget>[
            TextButton(
              child: const Text('Fechar'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Bora remover o fundo!',
          style: TextStyle(color: Colors.white),
        ),
        backgroundColor: Colors.blue,
        centerTitle: true,
      ),
      bottomNavigationBar: BottomNavigationBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.settings),
            label: 'Settings',
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              const SizedBox(height: 20),
              if (_image == null)
                ElevatedButton(
                  onPressed: _pickImage,
                  child: const Text('Selecione uma foto'),
                ),
              if (_image != null)
                Container(
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.grey),
                  ),
                  width: 300,
                  height: 300,
                  child: Image.file(_image!),
                ),
              if (_image != null) const SizedBox(height: 20),
              if (_image != null)
                ElevatedButton(
                  onPressed: _sendImage,
                  child: const Text('Remover fundo'),
                ),
              if (_processedImage != null) const SizedBox(height: 20),
              if (_processedImage != null)
                Container(
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.grey),
                  ),
                  width: 300,
                  height: 300,
                  child: Image.memory(_processedImage!),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
