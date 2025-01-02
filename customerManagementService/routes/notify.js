const express = require("express");
const router = express.Router();
require("dotenv").config();
const smsService = require("../controllers/sms");
const customerControllers = require("../controllers/customer.controllers");

router.post("/dapr/subscribe/notify", accountUpdate);

module.exports = router;
transaction = {
  customer_id: "1f2fdd06-f3a2-4047-94aa-c39bc09a17e3",
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
  console.log("Received message on updateAccount:", transaction["account_id"]);
  //smsService.handleTransactionCompletion(transaction);
  res.status(200).send("Received");
}
