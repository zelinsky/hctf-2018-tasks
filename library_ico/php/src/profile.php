<?php
require_once 'loader.php';
require_once 'database.php';

ensure_login();

$msg = "";
if ($_POST) {
    if (isset($_POST['password'])) {
        $u = new User(null);
        $res = $u->update(
            array(
                "password" => sha1($_POST['password']),
                "tags" => isset($_POST['tags']) ? $_POST['tags']  : serialize(array()), // for experimenting
            ),
            array(
                "uid" => array("=", $_SESSION['uid'])
            )
        );
        if ($res) {
            $msg = "Successfully updated!";
        } else {
            $msg = "Could not update user!";
        }
    }
}

$user = new User($_SESSION['uid']);
$user->refresh();
$template = $twig->load('profile.html');
echo $template->render(array("msg" => $msg, "user" => $user->obj));