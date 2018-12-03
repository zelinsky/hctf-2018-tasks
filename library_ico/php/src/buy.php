<?php
require_once 'loader.php';
require_once 'database.php';

ensure_login();

$product = "";

if (isset($_GET['id'])) {
    $p = new Product($_GET['id']);
    $p->refresh();
    $user = new User($_SESSION['uid']);
    $user->refresh();
    $balance = $user->calc_balance();

    if ($p->obj->price && $balance >= $p->obj->price) {
        $trans = unserialize($user->obj->transactions);
        $trans[] = array("from" => $user->obj->name, "to" => "Shop", "amount" => -1 * $p->obj->price);
        $user->update(
            array("transactions" => serialize($trans)),
            array("uid" => array("=", $_SESSION['uid']))
        );
        $product = $p->obj;
    }
    $template = $twig->load('buy.html');
    echo $template->render(
        array(
            "product" => $product,
            "user" => $_SESSION['logged_in']
        )
    );

}
