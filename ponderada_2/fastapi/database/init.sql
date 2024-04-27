-- Creating database
CREATE DATABASE IF NOT EXISTS banco;
USE banco;

-- Creating user table
CREATE TABLE IF NOT EXISTS user (
    userId INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Creating todo table
CREATE TABLE IF NOT EXISTS todo (
    todoId INT AUTO_INCREMENT PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status INT NOT NULL,
    priority INT NOT NULL,
    userId INT NOT NULL,
    FOREIGN KEY (userId) REFERENCES user(userId) ON DELETE CASCADE
);

INSERT INTO user (name, email, password)
VALUES ('teste', 'teste@teste.mail.com', 'teste123');