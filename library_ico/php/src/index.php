<?php
include 'loader.php';

$template = $twig->load('base.html');
echo $template->render(array("user" => $_SESSION['logged_in']));