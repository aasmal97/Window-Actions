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
const onActiveWindows = async (action, targetContext, customAction) => {
  const result = await determineActiveWindows(
    "Elgato\\StreamDeck\\Plugins\\com.arkyasmal.windowActions.sdPlugin"
  );
  const newEvent = {
    action: action,
    event: "sendToPropertyInspector",
    context: targetContext,
    payload: {
      action: customAction,
      result: result,
      targetContext: uuid,
    },
  };
  socket.send(JSON.stringify(newEvent));
};
const parseEvent = (evt) => {
  const evtObj = JSON.parse(evt.data);
  let { context: targetContext, payload } = evtObj;
  if (!payload) payload = {};
  let { action, settings } = payload;
  if (!settings) settings = {};
  const { type, name } = settings;
  return {
    targetContext,
    payload,
    action,
    settings,
    type,
    name,
  };
};
const respondToSubEvents = (evt) => {
  const { action, evtObj, targetContext } = respondToEvents(evt);
  switch (action) {
    case "com.arkyasmal.windowActions.openWindowGui":
      openGui();
      break;
    case "com.arkyasmal.windowActions.onActiveWindows":
      onActiveWindows(
        evtObj.action,
        targetContext,
        "com.arkyasmal.windowActions.activeWindows"
      );
      break;
    default:
      logEvent("Sub event does not match");
      break;
  }
};
const respondToKeyEvents = (evt) => {
  const { evtObj, type, name } = parseEvent(evt);
  switch (evtObj.action) {
    case "com.arkyasmal.windowActions.minimizeWindows":
      minimizeWindow(type, name);
      break;
    case "com.arkyasmal.windowActions.maximizeWindows":
      maximizeWindow(type, name);
      break;
    case "com.arkyasmal.windowActions.closeWindows":
      closeWindow(type, name);
      break;
    default:
      logEvent("Button press event does not match");
      logEvent(evtObj);
      break;
  }
};
const respondToEvents = (evt) => {
  const { action, evtObj } = parseEvent(evt);
  if (action) respondToSubEvents(evt);
  else if (evtObj.event == "keyDown") respondToKeyEvents(evt);
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
  };
  socket.onmessage = (evt) => respondToEvents(evt);
  socket.onclose = () => {};
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
