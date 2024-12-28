const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
require("dotenv").config();
const Customer = require("../models/customer");
const customerControllers = require("./customer.controllers");

async function authenticate({ email, password }) {
  const customer = await Customer.findOne({ where: { email } });
  if (customer && bcrypt.compareSync(password, customer.password)) {
    const token = jwt.sign(
      { customerId: customer.id },
      process.env.ACCESS_TOKEN_SECRET,
      {
        expiresIn: "10d",
      }
    );

    return { ...customer.toJSON(), token };
  }
}

function verifyToken(req, res) {
  return new Promise((resolve, reject) => {
    const token = req.cookies.token;
    if (!token) {
      console.log("No token provided");
      return res.status(401).json({ message: "No token provided" });
    }
    jwt.verify(token, process.env.ACCESS_TOKEN_SECRET, (err, decoded) => {
      if (err) {
        console.log("Failed to authenticate token");
        return res
          .status(403)
          .json({ message: "Failed to authenticate token" });
      }
      resolve(decoded);
    });
  });
}

function getTokenId(req) {
  const token = req.cookies.token;
  const decoded = jwt.verify(token, process.env.ACCESS_TOKEN_SECRET);
  return decoded.customerId;
}

module.exports = {
  verifyToken,
  getTokenId,
  authenticate,
};
