SET SESSION time_zone = "+8:00";
ALTER DATABASE CHARACTER SET "utf8";

DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS auth;
DROP TABLE IF EXISTS app;

CREATE TABLE auth (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    num VARCHAR(50) NOT NULL,
    money int(9) Default 0,
    auth_time int(9) Default 4,
    username text,
    mac text,
    time DATETIME NOT NULL
);

CREATE TABLE app (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name text NOT NULL,
    version float(7,4) NOT NULL,
    description text,
    download text NOT NULL,
    time DATETIME NOT NULL
);

CREATE TABLE admin (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    username VARCHAR(20) NOT NULL, 
    password VARCHAR(40) NOT NULL 
);
