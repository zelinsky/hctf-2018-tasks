<?php
include("flag.php");
if (isset($_GET['passwd'])) {
        if (hash("md5", $_GET['passwd']) == '0e514198428367523082236389979035')        {
                echo $flag;
        } 
} else {
    echo '<html><body><form method="get"><input type="text" name="passwd" value="password"><input type="submit" value="login" /></form></body></html>';
} 
?>

