const { exec, execFile } = require("child_process");
const path = require("path");
const fetchWindowsJson = require("./fetchWindowsJson");
const getTypeCommand = (byType, name) => {
  let typeCommand = [];
  switch (byType) {
    case "hWnd":
      typeCommand = ["handle", name];
      break;
    case "program_name":
      typeCommand = ["process", name];
      break;
    case "win_class":
      typeCommand = ["class", name];
      break;
    case "win_title":
      typeCommand = ["title", name]
      break;
    case 'win_ititle':
      typeCommand = ["ititle", name]
    default:
      break;
  }
  return typeCommand;
};
const execDirectory = path.join(__dirname, "../executables");
const batFilesDirectory = path.join(__dirname, "../batFiles");
const execFileError = (err, stdout, sterr) => {
  if (err) console.error(err, "error");
  if (stdout) console.log(stdout, "message");
  if (sterr) console.error(sterr, "sterr");
};
const minimizeWindow = (byType, name) => {
  const typeCommand = getTypeCommand(byType, name);
  const command = `${execDirectory}\\nircmd.exe`;
  execFile(command, ["win", "min", ...typeCommand], execFileError);
};
const maximizeWindow = (byType, name) => {
  const typeCommand = getTypeCommand(byType, name);
  const command = `${execDirectory}\\nircmd.exe`;
  execFile(command, ["win", "max", ...typeCommand], execFileError);
};
const closeWindow = (byType, name) => {
  const typeCommand = getTypeCommand(byType, name);
  const command = `${execDirectory}\\nircmd.exe`;
  execFile(command, ["win", "close", ...typeCommand], execFileError);
};
const moveWindow = (byType, name, coordinates, size) => {
  const typeCommand = getTypeCommand(byType, name);
  const command = `${execDirectory}\\nircmd.exe`;
  execFile(command, ["win", "move", ...typeCommand], execFileError);
}
const determineActiveWindows = async (appDataDirectory) => {
  const command = `${execDirectory}\\determineActiveWindows.exe`;
  execFile(command, ["--appDataDirectory", appDataDirectory], execFileError);
  return await fetchWindowsJson(appDataDirectory);
};
const openGui = () => {
  const command = `"${batFilesDirectory}"\\findWindow.bat`;
  exec(command, execFileError);
};

module.exports = {
  minimizeWindow,
  openGui,
  maximizeWindow,
  closeWindow,
  determineActiveWindows,
  moveWindow
};
