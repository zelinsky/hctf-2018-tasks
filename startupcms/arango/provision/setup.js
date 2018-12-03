var users = require("@arangodb/users");
require("@arangodb/users").save("dbuser@arango", "ladskjqoi3242", true);
db._createDatabase("user_db")
db._useDatabase("user_db")
db._create("users")
db.users.save({ user: "tim", passwd: "iamsoawesome", role: "user"})
users.grantDatabase("dbuser@arango", "user_db", "ro");
users.grantCollection("dbuser@arango", "user_db", "users", "ro");