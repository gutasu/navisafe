<?php
// login.php - Login i logout d'usuaris
 
require_once __DIR__ . '/db.php';
 
header('Content-Type: application/json');
session_start();
 
$body = json_decode(file_get_contents('php://input'), true);
 
// --- LOGOUT ---
if (isset($body['action']) && $body['action'] === 'logout') {
    session_destroy();
    echo json_encode(['ok' => true]);
    exit;
}
 
// --- LOGIN ---
$username = trim($body['username'] ?? '');
$password = $body['password'] ?? '';
 
if ($username === '' || $password === '') {
    echo json_encode(['ok' => false, 'error' => 'Omple tots els camps']);
    exit;
}
 
$db   = getDB();
$stmt = $db->prepare("SELECT * FROM users WHERE username = ?");
$stmt->execute([$username]);
$user = $stmt->fetch(PDO::FETCH_ASSOC);
 
if ($user && password_verify($password, $user['password_hash'])) {
    session_regenerate_id(true);
    $_SESSION['username'] = $user['username'];
    echo json_encode(['ok' => true, 'username' => $user['username']]);
} else {
    echo json_encode(['ok' => false, 'error' => 'Usuari o contrasenya incorrectes']);
}