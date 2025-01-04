const { Sequelize } = require("sequelize");
const path = require("path");
require("dotenv").config();
const db_name = process.env.customers_db_name || "customers";
const customer = process.env.customers_db_mysql || "root";
const password = process.env.password_db_mysql || "admin";
const sequelize = new Sequelize(db_name, customer, password, {
  dialect: "mysql",
  host: process.env.MYSQL_HOST,
  port: 3306,
});
module.exports = sequelize;
