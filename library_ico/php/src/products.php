<?php
require_once 'loader.php';
require_once 'database.php';

ensure_login();

$p = new Product(null);
$res = $p->get_values(array("*"), array());
$products = array();

while ($row = $res->fetch_assoc()) {
    $products[] = $row;
}

$template = $twig->load('list.html');
echo $template->render(array("products" => $products, "user" => $_SESSION["logged_in"]));