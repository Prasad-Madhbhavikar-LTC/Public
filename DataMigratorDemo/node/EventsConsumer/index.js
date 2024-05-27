const express = require("express");
const { Kafka } = require("kafkajs");
const WebSocket = require("ws");
const cors = require("cors");
const { Partitioners } = require("kafkajs");

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

      WebSocket.WebSocketServer.clients.array.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(messageValue);
        }
      });
    },
  });
};

runConsumer().catch(console.error);

const wsServer = new WebSocket.Server({ noServer: true });

wsServer.on("connection", (ws) => {
  console.log("Websoket connection established");
});

const server = app.listen(port, () => {
  wsServer.handleUpgrade(request, socket, head, (socket) => {
    wsServer.emit("connection", socket, request);
  });
});
