<?php
require_once 'loader.php';


abstract class DBModel {
    public $obj;

    function __construct()
    {
        $this->obj = new stdClass;
    }

    function check_permission($mode) {
        $q = "SELECT r,w FROM permissions WHERE table_name='{$this->table}' and role='{$_SESSION['role']}'";
        $res = $this->query($q);
        $row = $res->fetch_assoc();
        if ($row[$mode] != 1) {
            throw new Exception("User does not have permission for query!");
        }
    }

    private function query($q) {
        global $db; // we want only one connection per user
        return $db->query($q);
    }

    private function last_id() {
        global $db;
        return $db->insert_id;
    }

    private function escape($f) {
        global $db;
        return $db->escape_string($f);
    }

    function get_values($fields, $filters) {
        $this->check_permission("r");
        $q_fields = implode(",", $fields);
        $q_where = array();
        foreach ($filters as $key => $value) {
            $q_where[] = $key . $value[0] . "'{$this->escape($value[1])}'";
        }
        $q_where = implode(" AND ", $q_where);
        if ($q_where) {
            $q_where = " WHERE " . $q_where;
        }
        $q = "SELECT $q_fields FROM {$this->table} $q_where";
        $res = $this->query($q);
        return $res;
    }

    function populate_members($fields, $filters) {
        $res = $this->get_values($fields, $filters);
        $this->obj = (object) $res->fetch_assoc();
    }

    function create($fields) {
        $this->check_permission("w");
        $q_fields = array();
        $q_vals = array();
        foreach ($fields as $k => $v) {
            $q_fields[] = $k;
            $q_vals[] = "'{$this->escape($v)}'";
        }
        $q_f = implode(", ", $q_fields);
        $q_v = implode(", ", $q_vals);
        $q = "INSERT INTO {$this->table} ($q_f) VALUES ($q_v)";
        $this->query($q);
        return $this->last_id();
    }

    function update($fields, $filters) {
        $this->check_permission("w");
        $q_fields = array();
        foreach ($fields as $k => $v) {
            $q_fields[] = "$k='{$this->escape($v)}'";
        }
        $q_f = implode(", ", $q_fields);
        $q_where = "";
        foreach ($filters as $key => $value) {
            $q_where = $q_where .$key . $value[0] . "'{$this->escape($value[1])}'";
        }
        $q = "UPDATE {$this->table} SET $q_f WHERE $q_where";
        $res = $this->query($q);
        return $res;
    }
}

class User extends DBModel {
    public $table = "users";
    public $uid;

    static function factory($name, $password, $tags) {
        $u = new User(null);
        $uid = $u->create(
            array(
                "name" => $name,
                "password" => sha1($password),
                "transactions" => serialize(array()),
                "tags" => serialize($tags)
                )
        );
        $u->uid = $uid;
        $u->refresh();
        return $u;
    }

    function __construct($uid)
    {
        parent::__construct();
        $this->uid = $uid;
    }

    function refresh() {
        $this->populate_members(array("*"), array("uid" => array("=", $this->uid)));
    }

    function calc_balance() {
        $this->refresh();
        $trans = unserialize($this->obj->transactions);
        $balance = 0;
        foreach ($trans as $t) {
            $balance += $t['amount'];
        }
        return $balance;
    }

    function __toString()
    {
        $this->refresh();
        return $this->obj->name;
    }
}

class Gift extends DBModel {
    public $table = "gifts";
}

class Product extends DBModel{
    public $table = "products";
    public $pid;

    function __construct($pid)
    {
        parent::__construct();
        $this->pid = $pid;
    }

    function refresh() {
        $this->populate_members(array("*"), array("pid" => array("=", $this->pid)));
    }
}