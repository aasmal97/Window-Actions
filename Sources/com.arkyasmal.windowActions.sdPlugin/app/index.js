const WebSocket = require("ws");
const { program } = require("commander");
const {
  minimizeWindow,
  openGui,
  maximizeWindow,
  closeWindow,
  determineActiveWindows,
} = require("./nodeExecCommands/commands.js");
const path = require("path");
const fs = require("fs");
let socket = null;
let uuid = null;
const dataDirectory = process.env.APPDATA;
const filePath = path.join(
  dataDirectory,
  "Elgato\\StreamDeck\\Plugins\\com.arkyasmal.windowActions.txt"
);
const logEvent = (payload) => {
  const json = {
    event: "logMessage",
    payload: typeof payload === "string" ? { message: payload } : payload,
  };
  const new_payload = JSON.stringify(json);
  //wrtie to a text file
  fs.appendFileSync(filePath, new_payload);
  socket.send(new_payload);
};
//elgato initialization
const onActiveWindows = async (action) => {
  const result = await determineActiveWindows(
    "Elgato\\StreamDeck\\Plugins\\com.arkyasmal.windowActions.sdPlugin"
  );
  const newEvent = {
    action: action,
    event: "sendToPropertyInspector",
    context: uuid,
    payload: result,
  };
  socket.send(JSON.stringify(newEvent));
};
const respondToEvents = (evt) => {
  const evtObj = JSON.parse(evt.data);
  let { payload } = evtObj;
  if (!payload) payload = {};
  let { action, settings } = payload;
  if (!settings) settings = {};
  const { type, name } = settings;
  switch (action) {
    case "com.arkyasmal.windowActions.minimizeWindows":
      minimizeWindow(type, name);
      break;
    case "com.arkyasmal.windowActions.maximizeWindows":
      maximizeWindow(type, name);
      break;
    case "com.arkyasmal.windowActions.closeWindows":
      closeWindow(type, name);
      break;
    case "com.arkyasmal.windowActions.openWindowGui":
      openGui();
      break;
    case "com.arkyasmal.windowActions.onActiveWindows":
      onActiveWindows(evtObj.action);
      break;
    default:
      logEvent("didn't match any conditions");
      logEvent(evtObj);
      break;
  }
};
const registerSocket = (inRegisterEvent) => {
  let event;
  try {
    event = JSON.parse(inRegisterEvent);
  } catch (e) {
    event = inRegisterEvent;
  }
  const registerData = {
    event,
    uuid,
  };
  socket.send(JSON.stringify(registerData));
};

function connectElgatoStreamDeckSocket(
  inPort,
  inPluginUUID,
  inRegisterEvent,
  inInfo
) {
  socket = new WebSocket("ws://127.0.0.1:" + inPort);
  uuid = inPluginUUID;
  socket.onopen = () => {
    registerSocket(inRegisterEvent);
    logEvent("Successfully Connected");
  };
  socket.onmessage = (evt) => respondToEvents(evt);
  socket.onclose = () => logEvent("Successfully disconnected");
}
//main function to be called in command line
if (typeof require !== "undefined" && require.main === module) {
  program
    .option("-port, --port <port>", "Port number")
    .option("-pluginUUID, --pluginUUID <uuid>", "plugin unique id")
    .option(
      "-registerEvent, --registerEvent <event>",
      "event needed to register plugin"
    )
    .option("-info, --info <info>", "StreamDeck device info")
    .parse();
  const mapOfArgs = program.opts();
  connectElgatoStreamDeckSocket(
    mapOfArgs.port,
    mapOfArgs.pluginUUID,
    mapOfArgs.registerEvent,
    mapOfArgs.info
  );
}
module.exports = connectElgatoStreamDeckSocket;
