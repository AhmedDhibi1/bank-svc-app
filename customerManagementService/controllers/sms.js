const axios = require("axios");
require("dotenv").config();
const Customer = require("../models/customer");
const customerController = require("./customer.controllers");

async function sendSMS(customerPhoneNumber, transactionDetails) {
  const smsPayload = {
    metadata: {
      toNumber: customerPhoneNumber,
    },
    data: `Transaction Successful! Amount: ${transactionDetails.amount}, Date: ${transactionDetails.created_at}`,
    operation: "create",
  };

  try {
    await axios.post(process.env.dapr_bindings, smsPayload);
    console.log("SMS sent successfully");
  } catch (error) {
    console.error("Failed to send SMS:", error);
  }
}

async function handleTransactionCompletion(transaction) {
  try {
    const customer = customerController.getById(transaction["customer_id"]);
    const customerPhoneNumber = customer["phone"];
    await sendSMS(customerPhoneNumber, transaction);
  } catch (error) {
    console.error("Error sending SMS:", error);
  }
}

module.exports = { handleTransactionCompletion };
