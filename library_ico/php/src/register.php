<?php
include 'loader.php';
include 'database.php';

$msg = "";
if ($_POST) {
    if (isset($_POST['name']) && isset($_POST['password'])) {
        $u = new User(null);
        $res = $u->create(
            array(
                "name" => $_POST['name'],
                "password" => sha1($_POST['password']),
                "transactions" => serialize(array()),
                "tags" => serialize(array()), // Hash tags will be supported in future releases
                "got_gift" => 0
            )
        );
        if ($res) {
            $msg = "Successful, you can now login!";
        } else {
            $msg = "Could not create user, username taken!";
        }
    }
}

$template = $twig->load('register.html');
echo $template->render(array("msg" => $msg));