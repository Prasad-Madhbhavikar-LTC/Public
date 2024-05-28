const express = require("express");
const { Kafka } = require("kafkajs");
const WebSocket = require("ws");
const cors = require("cors");

const app = express();
const port = 3000;

app.use(cors());

const kafka = new Kafka({ clientId: "My-app", brokers: ["localhost:9092"] });

const consumer = kafka.consumer({ groupId: "test-group" });

const runConsumer = async () => {
  await consumer.connect();
  await consumer.subscribe({
    topic: "processing_progress_events_topic",
    fromBeginning: true,
  });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const messageValue = message.value.toString();
      console.log({
        partition: partition,
        offset: message.offset,
        value: messageValue,
      });

      wss.clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(messageValue);
        }
      });
    },
  });
};

runConsumer().catch(console.error);

const wss = new WebSocket.Server({ noServer: true });

wss.on("connection", (ws) => {
  console.log("WebSocket connection established");
});

wss.on("close", () => {
  console.log("WebSocket connection closed");
});

const server = app.listen(port, () => {
  server.on("upgrade", (request, socket, head) => {
    wss.handleUpgrade(request, socket, head, (ws) => {
      wss.emit("connection", ws, request);
      console.log("Connection upgrade complete");
    });
  });

  console.log(`Express server listening on port ${port}`);
});
