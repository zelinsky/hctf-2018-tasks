<?php
require_once 'loader.php';
require_once 'database.php';

ensure_login();

$msg = "";

if (isset($_GET['do'])) {
    $gift = new Gift();
    $res_gift = $gift->get_values(
        array("*"),
        array("uid" => array("=", $_SESSION['uid']))
    );

    if (!$res_gift->num_rows) {
        $user = new User($_SESSION['uid']);
        $user->refresh();
        $trans = unserialize($user->obj->transactions);
        $trans[] = array("from" => "Welcome Gift", "to" => $user->obj->name, "amount" => "500");
        $user->update(
            array("transactions" => serialize($trans)),
            array("uid" => array("=", $_SESSION['uid']))
        );
        $gift->create(array("uid" => $_SESSION['uid']));
        header("Location: transactions.php");
        die();
    } else {
        $msg = "You already received your free coins!";
    }
}

$user = new User($_SESSION['uid']);
$user->refresh();

$template = $twig->load('free.html');
echo $template->render(
    array(
        "user" => $user,
        "msg" => $msg
    )
);