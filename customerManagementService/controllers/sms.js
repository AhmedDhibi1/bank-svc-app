const axios = require("axios");
require("dotenv").config();
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
    // Get the customer info (assuming transaction has a customer_id)
    const customer = await customerController.getById(transaction.customer_id);
    const customerPhoneNumber = customer.phone;
    console.log(`Sending SMS to: ${customerPhoneNumber}`);

    // Send SMS with transaction details
    await sendSMS(customerPhoneNumber, transaction);
  } catch (error) {
    console.error(
      "Error handling transaction completion:",
      error.message || error
    );
  }
}

module.exports = { handleTransactionCompletion };
