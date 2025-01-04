const { DaprClient, DaprServer } = require("@dapr/dapr");
const { HttpMethod } = require("@dapr/dapr").types;

// Initialize the Dapr client
const daprClient = new DaprClient();

// Initialize the Dapr server
const daprServer = new DaprServer(daprClient);

// Subscribe to a topic
async function subscribe() {
  // Create an HTTP handler for incoming messages on the subscribed topic
  daprServer.app.post("/my-topic", async (req, res) => {
    const message = req.body;
    console.log("Received message:", message);

    // Acknowledge the message
    res.status(200).send("OK");
  });

  // Start the Dapr server
  await daprServer.start();
  console.log("Dapr Subscriber is running...");
}

// Start the subscription
subscribe().catch(console.error);
