<?php
require_once 'loader.php';

ensure_login();


$template = $twig->load('ico.html');
echo $template->render(array("user" => true));


