const express = require("express");
const router = express.Router();
require("dotenv").config();
const smsService = require("../controllers/sms");
const customerControllers = require("../controllers/customer.controllers");

router.post("/dapr/subscribe/notify", accountUpdate);

module.exports = router;
Transaction = {
  customer_id: "88edaf02-d912-4ae5-8df9-22da06355ab2",
  account_id: " 8e2ccf91-6bc5-47bb-81e6-0b3fbb828b5b",
  amount: 100,
  operation: "debit",
  transaction_type: "DEPOSIT",
  status: "COMPLETED",
  timestamp: "2024-12-31T17:51:59.748427",
};
function accountUpdate(req, res) {
  const cloudEvent = req.body;
  const transaction = cloudEvent.data;
  console.log(transaction);
  console.log("Received message on updateAccount:", transaction["account_id"]);
  smsService.handleTransactionCompletion(transaction);
  res.status(200).send("Received");
}
