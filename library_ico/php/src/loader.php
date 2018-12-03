<?php
require_once 'vendor/autoload.php';

// Session
session_start();
if (!isset($_SESSION['role'])) {
    $_SESSION['role'] = "guest";
    $_SESSION['logged_in'] = false;
}

function ensure_login() {
    if (!$_SESSION['logged_in']){
        header("Location: index.php");
        die();
    }
}

// Templating
$loader = new Twig_Loader_Filesystem('templates');
$twig = new Twig_Environment($loader); // TODO: caching

//DB
$db = new mysqli("db", "pwncoin", "Ahd92uaj99ADAD", "pwncoin");

if ($db->connect_errno) {
    throw new mysqli_sql_exception( "Failed to connect to MySQL: " . $db->connect_error);
}
