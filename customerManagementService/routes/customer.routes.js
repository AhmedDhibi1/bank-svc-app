const express = require("express");
const router = express.Router();
const customerControllers = require("../controllers/customer.controllers");
const AuthControllers = require("../controllers/auth.controllers");
const Customer = require("../models/customer");

const jwt = require("jsonwebtoken");
require("dotenv").config();

router.post("/authenticate", authenticate);
router.post("/register", register);
router.get("/getAll", getAll);
router.get("/current", getCurrent);
router.get("/:id", getById);
router.put("/:id", update);
router.delete("/:id", _delete);

module.exports = router;

function authenticate(req, res, next) {
  AuthControllers.authenticate(req.body)
    .then((customer) => {
      customer
        ? res.json({
            customer: customer,
            message: "Customer logged in successfully",
          })
        : res.status(400).json({ message: "email or password is incorrect." });
    })
    .catch((error) => next(error));
}

function register(req, res, next) {
  // Ensure that req.body contains all required properties
  if (!req.body || !req.body.email || !req.body.password) {
    return res.status(400).json({ message: `Invalid request body` });
  }

  customerControllers
    .create(req.body)
    .then((customer) =>
      res.json({
        customer: customer,
        message: `Customer Registered successfully with email ${req.body.email}`,
      })
    )
    .catch((error) => next(error));
}
async function getAll(req, res, next) {
  try {
    const customers = await customerControllers.getAll(req, res);
    res.json(customers);
  } catch (err) {
    // Handle errors appropriately
    res.status(401).json({ message: "Not Authorized!" });
  }
}

function getCurrent(req, res, next) {
  // Extract the token from the request headers
  const token = req.cookies.token;

  // Decode the token to access the payload
  const decodedToken = jwt.decode(token);

  // Check if the decoded token contains the customer ID
  if (!decodedToken || !decodedToken.customerId) {
    return res.status(401).json({ message: "Unauthorized" });
  }

  // Pass the customer ID to the getById function
  customerControllers
    .getById(decodedToken.customerId)
    .then((customer) => {
      if (!customer) {
        return res.status(404).json({ message: "Customer not found" });
      }
      res.json(customer);
    })
    .catch((error) => next(error));
}

function getById(req, res, next) {
  customerControllers
    .getById(req.params.id)
    .then((customer) => {
      if (!customer) {
        console.log(customer);
        res.status(404).json({ message: "Customer Not Found!" });
        next();
      }

      return res.json(customer);
    })
    .catch((error) => next(error));
}

function update(req, res, next) {
  console.log("req.body:", req.body);
  customerControllers
    .update(req.params.id, req.body)
    .then(() => {
      res.json({
        message: `Customer with id: ${req.params.id} updated successfully.`,
      });
      console.log(`Customer with id: ${req.params.id} updated successfully.`);
    })
    .catch((error) => next(error));
}

function _delete(req, res, next) {
  customerControllers
    .delete(req.params.id)
    .then(() =>
      res.json({
        message: `Customer with id: ${req.params.id} deleted successfully.`,
      })
    )
    .catch((error) => next(error));
}
