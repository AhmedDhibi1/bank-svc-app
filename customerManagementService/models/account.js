const { DataTypes, Model } = require("sequelize");
const sequelize = require("../config/database"); // Adjust the path to your database configuration

class Account extends Model {}

Account.init({
  accountId: {
    type: DataTypes.STRING,
    primaryKey: true,
  },
  accountType: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  accountOpeningDate: {
    type: DataTypes.DATE,
    allowNull: false,
  },
  lastActivity: {
    type: DataTypes.DATE,
    allowNull: true,
  },
  balance: {
    type: DataTypes.INTEGER,
    allowNull: false,
    defaultValue: 0,
  },
  customerId: {
    type: DataTypes.STRING,
    allowNull: false,
  },
});

module.exports = Account;
