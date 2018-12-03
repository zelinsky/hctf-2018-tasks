<?php
require_once 'loader.php';

ensure_login();
unset($_SESSION['uid']);
$_SESSION['logged_in'] = false;
$_SESSION['role'] = "guest";

header("Location: index.php");
die();