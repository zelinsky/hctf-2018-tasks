<?php
require_once 'loader.php';
require_once 'database.php';

$msg = "";
if ($_POST) {
    if (isset($_POST['name']) && isset($_POST['password'])) {
        $u = new User(null);
        $res = $u->get_values(
            array("uid"),
            array(
                "name" => array("=", $_POST['name']),
                "password" => array("=", sha1($_POST['password']))
            )
        );
        if (!$res->num_rows) {
            $msg = "Username/Password not correct!";
        } else {
            $_SESSION['uid'] = $res->fetch_assoc()['uid'];
            $_SESSION['role'] = "user";
            $_SESSION['logged_in'] = true;
            header("Location: index.php");
            die();
        }
    }
} else {
    $msg = "Inavlid form data.";
}

$template = $twig->load('login_fail.html');
echo $template->render(array("msg" => $msg));