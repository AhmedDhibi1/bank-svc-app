const express = require("express");
const router = express.Router();
require("dotenv").config();
const smsService = require("../controllers/sms");
const customerControllers = require("../controllers/customer.controllers");

router.post("/dapr/subscribe/notify", accountUpdate);

module.exports = router;

function accountUpdate(req, res) {
  const cloudEvent = req.body;
  const transaction = cloudEvent.data;
  console.log("Received message on updateAccount:", transaction["account_id"]);
  smsService.handleTransactionCompletion(transaction);
  res.status(200).send("Received");
}
