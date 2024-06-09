class User {
  final String email;
  final String password;

  User({required this.email, required this.password});

  Map<String, String> toJson() {
    return {
      'email': email,
      'password': password,
    };
  }
}
