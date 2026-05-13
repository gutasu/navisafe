<?php

 
function getDB() {
    if (!is_dir(__DIR__ . '/../data')) {
        mkdir(__DIR__ . '/../data', 0755, true);
    }
 
    $db = new PDO('sqlite:' . __DIR__ . '/../data/navisafe.db');
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
 
    
    $db->exec("CREATE TABLE IF NOT EXISTS users (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        username      TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    )");
 
  
    $usuaris = [
        ['admin',   'navisafe'],
        ['guillem', '123'],
        ['miquel',  '123'],
    ];
 
    foreach ($usuaris as [$nom, $contrasenya]) {
        $check = $db->prepare("SELECT id FROM users WHERE username = ?");
        $check->execute([$nom]);
        if (!$check->fetch()) {
            $hash = password_hash($contrasenya, PASSWORD_BCRYPT);
            $ins  = $db->prepare("INSERT INTO users (username, password_hash) VALUES (?, ?)");
            $ins->execute([$nom, $hash]);
        }
    }
 
    return $db;
}