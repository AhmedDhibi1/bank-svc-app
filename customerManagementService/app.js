const express = require("express");
const cors = require("cors");
const sequelize = require("./config/db_config");
const app = express();
const customersRouter = require("./routes/customer.routes");
const notifyRouter = require("./routes/notify");
const Customer = require("./models/customer");
const bodyParser = require("body-parser");
app.use(bodyParser.json({ type: "application/cloudevents+json" }));
const axios = require("axios");
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());

app.use(`/customers`, customersRouter);
app.use(``, notifyRouter);

app.post("/dapr/subscribe/notify", (req, res) => {
  const cloudEvent = req.body;
  const eventData = cloudEvent.data;
  console.log("Received message on updateAccount:", eventData["accountId"]);
  res.status(200).send("Received");
});
app.post("/dapr/subscribe/updateAccount", (req, res) => {
  const cloudEvent = req.body;
  const eventData = cloudEvent.data;
  console.log("Received message on updateAccount:", eventData["accountId"]);
  res.status(200).send("Received");
});
transaction = {
  amount: 100.0,
  transaction_type: "TRANSFER",
  from_account: "1f2fdd06-f3a2-4047-94aa-c39bc09a17e3",
  to_account: "8e2ccf91-6bc5-47bb-81e6-0b3fbb828b5b",
  description: "loan",
  transaction_id: "a5855f22-12e6-440c-ad9d-63f778104000",
  status: "COMPLETED",
  created_at: "2024-12-31T17:51:59.748421",
  updated_at: "2024-12-31T17:51:59.748427",
};
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
// Sync models with the database
sequelize
  .sync()
  .then(() => {
    console.log("Models synchronized with the database.");
  })
  .catch((error) => {
    console.error("Error synchronizing models:", error);
  });

// Use the HTTP server to listen for requests
app.listen(process.env.APP_PORT, () =>
  console.log(`Server is listening on PORT: ${process.env.APP_PORT}`)
);
async function handleTransactionCompletion(transaction) {
  try {
    await sendSMS("+21628803469", transaction);
  } catch (error) {
    console.error("Error sending SMS:", error);
  }
}

//handleTransactionCompletion(transaction);
