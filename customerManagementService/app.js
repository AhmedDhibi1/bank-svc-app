const { DaprClient, CommunicationProtocolEnum } = require("@dapr/dapr");
const express = require("express");
const cors = require("cors");
const sequelize = require("./config/db_config");
const app = express();
const customersRouter = require("./routes/customer.routes");
const Customer = require("./models/customer");

const daprHost = "http://localhost";
const daprPort = "3500"; // Default Dapr HTTP port
const daprClient = new DaprClient(daprHost, daprPort, CommunicationProtocolEnum.HTTP);

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());

app.use(`/customers`, customersRouter);



// sequelize
//   .sync()
//   .then(() => {
//     app.listen(process.env.API_CUSTOMERS_PORT, () => {
//       console.log(`App is listening PORT: ${process.env.API_CUSTOMERS_PORT}`);
//     });
//   })
//   .catch((err) => {
//     return res.status(403).json({ notice: err.message, status: "NO" });
//   });

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
