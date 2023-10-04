const { execFile } = require("child_process");
const path = require("path");
const fetchWindowsJson = require("./fetchWindowsJson");
const execDirectory = path.join(__dirname, "../pluginActions");
const execFileError = (err, stdout, sterr) => {
  if (err) console.error(err, "error");
  if (stdout) console.log(stdout, "message");
  if (sterr) console.error(sterr, "sterr");
};
const minimizeWindow = (byType, name) => {
  const typeCommand = ["--winIdType", byType, "--winId", name];
  const command = `${execDirectory}\\pluginActions.exe`;
  execFile(
    command,
    ["--action", "minimize_window", ...typeCommand],
    execFileError
  );
};
const maximizeWindow = (byType, name) => {
  const typeCommand = ["--winIdType", byType, "--winId", name];
  const command = `${execDirectory}\\pluginActions.exe`;
  execFile(
    command,
    ["--action", "maximize_window", ...typeCommand],
    execFileError
  );
};
const closeWindow = (byType, name) => {
  const typeCommand = ["--winIdType", byType, "--winId", name];
  const command = `${execDirectory}\\pluginActions.exe`;
  execFile(
    command,
    ["--action", "close_window", ...typeCommand],
    execFileError
  );
};
const resizeWindow = (byType, name, coordinates, size) => {
  const typeCommand = ["--winIdType", byType, "--winId", name];
  const command = `${execDirectory}\\pluginActions.exe`;
  let coordinatesArr = [0, 0];
  if (coordinates) coordinatesArr = [coordinates.x, coordinates.y];
  let sizeArr = [];
  if (size) sizeArr = [size.width, size.height];
  const cliArgs = [
    "--action",
    "resize_window",
    ...typeCommand,
    "--coordinates",
    coordinatesArr.toString(),
    "--size",
    sizeArr.toString(),
  ];
  execFile(command, cliArgs, execFileError);
};
const determineActiveWindows = async (appDataDirectory) => {
  const command = `${execDirectory}\\pluginActions.exe`;
  execFile(
    command,
    ["--action", "get_active_windows", "--appDataDirectory", appDataDirectory],
    execFileError
  );
  return await fetchWindowsJson(appDataDirectory, "activeWindows.json");
};
const moveWindowsVirtualDesktops = async (byType, name, newDesktop) => {
  const command = `${execDirectory}\\pluginActions.exe`;
  const params = [
    "--winIdType",
    byType,
    "--winId",
    name,
    "--newDesktop",
    newDesktop,
  ];
  execFile(command, ["--action", "move_window", ...params], execFileError);
};
const moveVirtualDesktops = async (newDesktop) => {
  const command = `${execDirectory}\\pluginActions.exe`;
  const params = ["--newDesktop", newDesktop];
  execFile(
    command,
    ["--action", "move_virtual_desktop", ...params],
    execFileError
  );
};
const createVirtualDesktops = async (numOfNewDesktops) => {
  const command = `${execDirectory}\\pluginActions.exe`;
  const params = ["--numOfNewDesktops", numOfNewDesktops];
  execFile(command, ["--action", "create_desktop", ...params], execFileError);
};
const moveWindowToNewMonitor = async (byType, name, newMonitor) => {
  const command = `${execDirectory}\\pluginActions.exe`;
  const params = [
    "--winIdType",
    byType,
    "--winId",
    name,
    "--newMonitor",
    newMonitor,
  ];
  execFile(
    command,
    ["--action", "move_window_to_monitor", ...params],
    execFileError
  );
};
const getMonitorInfo = async (appDataDirectory) => {
  const command = `${execDirectory}\\pluginActions.exe`;
  const params = ["--appDataDirectory", appDataDirectory];
  execFile(command, ["--action", "get_monitor_info", ...params], execFileError);
  return await fetchWindowsJson(appDataDirectory, "currentMonitors.json");
};
const toggleThroughVirtualMonitors = async (direction) => {
  const command = `${execDirectory}\\pluginActions.exe`;
  const params = ["--direction", direction];
  execFile(
    command,
    ["--action", "move_by_one_virtual_desktop", ...params],
    execFileError
  );
};

module.exports = {
  getMonitorInfo,
  minimizeWindow,
  maximizeWindow,
  closeWindow,
  determineActiveWindows,
  resizeWindow,
  moveWindowsVirtualDesktops,
  moveVirtualDesktops,
  createVirtualDesktops,
  moveWindowToNewMonitor,
  toggleThroughVirtualMonitors,
};
