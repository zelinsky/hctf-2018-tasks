<?php
require_once 'loader.php';
require_once 'database.php';

ensure_login();

$user = new User($_SESSION['uid']);
$user->refresh();
$template = $twig->load('transactions.html');
$trans = unserialize($user->obj->transactions);
$balance = $user->calc_balance();
echo $template->render(
    array(
        "user" => $user->obj,
        "transactions" => $trans,
        "balance" => $balance,
        "tags" => unserialize($user->obj->tags)
    )
);