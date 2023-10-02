const createOption = (value, textContent) => {
  const newOption = document.createElement("option");
  newOption.value = value;
  newOption.textContent = textContent;
  return newOption;
};
const createDefaultOption = (textContent) => {
  const defaultOption = createOption("", textContent);
  defaultOption.selected = true;
  defaultOption.disabled = true;
  defaultOption.value = "";
  return defaultOption;
};
const selectedTypeChange = (event) => {
  const value = event.currentTarget.value;
  saveSettings({ key: "type", value: value });
  sendValueToPlugin("com.arkyasmal.windowActions.onActiveWindows", "action");
};
const onIdChange = (value) => {
  saveSettings({ key: "value", value: { name: value } });
};
const onIdTypeChange = (event) => {
  const identiferDropdown = document.getElementById("identifer_dropdown");
  const identiferText = document.getElementById("identifer_text");
  const value = event.currentTarget.value;
  if (value === "text") {
    identiferDropdown.style = "display:none;";
    identiferText.style = "";
    saveSettings({ key: "identifer_text", value: "true" });
  } else {
    identiferDropdown.style = "";
    identiferText.style = "display:none";
    saveSettings({ key: "identifer_text", value: "false" });
  }
  //clear all settings
  identiferDropdown.value = "";
  identiferText.value = "";
  const prevName = settings.value
    ? settings.value.name
      ? settings.value.name
      : settings.name
    : settings.name;
  const prevSettings = settings.value ? settings.value : {};
  saveSettings({ key: "value", value: { ...prevSettings, name: prevName } });
};
const removeChildNodes = (el) => {
  while (el.hasChildNodes()) {
    el.removeChild(el.lastChild);
  }
  return el;
};
const modifyDropdownActiveWindowInputs = (payload) => {
  const winTypeInput = document.getElementById("select_win_type");
  const identiferDropdown = document.getElementById("identifer_dropdown");
  const typeInput = winTypeInput.value;
  const activeWindows = payload;
  const defaultOption = createDefaultOption("--Select Identifer--");
  const options = activeWindows.map((window) => {
    const value =
      typeInput === "win_title" || typeInput === "win_ititle"
        ? window.title
        : window[typeInput];
    const text = `${value} (${window.title})`;
    return createOption(value, text);
  });
  options.unshift(defaultOption);
  //replace children with new ones
  removeChildNodes(identiferDropdown);
  identiferDropdown.append(...options);
};
const modifyMonitorInputs = (payload, currValue) => {
  const monitors = payload;
  const identiferDropdown = document.getElementById(
    "move_windows_to_monitor_select"
  );
  const options = monitors.map((monitor) => {
    const value = monitor.idx;
    const text = `${monitor.name} (Desktop ${value})`;
    return createOption(value, text);
  });
  identiferDropdown.append(...options);
  const newValue = currValue ? currValue : monitors[0].idx
  identiferDropdown.value =  newValue;
  onValueInputChange('newMonitor', newValue)
};
const respondToEvents = (evt) => {
  const { payload } = evt;
  const { action, result } = payload;
  switch (action) {
    case "com.arkyasmal.windowActions.activeWindows":
      modifyDropdownActiveWindowInputs(result);
      break;
    case "com.arkyasmal.windowActions.getmonitorinfo":
      modifyMonitorInputs(result, settings?.value?.newMonitor);
    default:
      return;
  }
};
const openInDefaultBrowser = (event) => {
  event.preventDefault();
  const target = event.target;
  const url = target.href;
  const urlPayload = {
    event: "openUrl",
    payload: {
      url: url,
    },
  };
  $SD.connection.send(JSON.stringify(urlPayload));
};

const onResizeInputChange = (inputType, key, value) => {
  if (!settings || !inputType || !key || (typeof value === "string" && !value))
    return;
  const prevValue = settings.value ? settings.value : {};
  const prevInputVal = prevValue
    ? prevValue[inputType]
      ? prevValue[inputType]
      : {}
    : {};
  const currVal = {
    ...prevValue,
    [inputType]: {
      ...prevInputVal,
      [key]: parseFloat(value),
    },
  };
  saveSettings({
    key: "value",
    value: currVal,
  });
};
const onValueInputChange = (inputType, value) => {
  if (!settings || !inputType || (typeof value === "string" && !value)) return;
  const prevValue = settings.value ? settings.value : {};
  const currVal = {
    ...prevValue,
    [inputType]: value,
  };
  saveSettings({
    key: "value",
    value: currVal,
  });
};
/**
 * The 'connected' event is the first event sent to Property Inspector, after it's instance
 * is registered with Stream Deck software. It carries the current websocket, settings,
 * and other information about the current environmet in a JSON object.
 * You can use it to subscribe to events you want to use in your plugin.
 */
const changeIdDom = (value) => {
  const identiferText = document.getElementById("identifer_text");
  const identiferDropdown = document.getElementById("identifer_dropdown");
  const identiferTextRadio = document.getElementById("identifer_text_type");
  const identiferDropdownRadio = document.getElementById(
    "identifer_dropdown_type"
  );
  identiferDropdownRadio.checked = false;
  identiferTextRadio.checked = true;
  identiferText.style = "";
  identiferDropdown.style = "display: none;";
  identiferText.value = value.name;
};
const changeResizeInputsDom = (value) => {
  if (!value) return;
  const coordinatesX = document.getElementById("window_coord_x");
  const coordinatesY = document.getElementById("window_coord_y");
  const sizeWidth = document.getElementById("window_size_width");
  const sizeHeight = document.getElementById("window_size_height");
  const coordinates = value.coordinates;
  const size = value.size;
  coordinatesX.value = coordinates ? (coordinates.x ? coordinates.x : 0) : 0;
  coordinatesY.value = coordinates ? (coordinates.y ? coordinates.y : 0) : 0;
  sizeWidth.value = size ? (size.width ? size.width : "") : "";
  sizeHeight.value = size ? (size.height ? size.height : "") : "";
};
const determineContainerStyles = (action) => {
  const wrapper = document.getElementById("window_specific_inputs");
  //we need to input new input values
  switch (action) {
    case "com.arkyasmal.windowactions.resizewindows":
      const resizeWindowInputs = document.getElementById(
        "resize_window_inputs_container"
      );
      resizeWindowInputs.style = "width: 100%";
      wrapper.style = "";
      break;
    case "com.arkyasmal.windowactions.movevirtualdesktops":
      const navigateVirtualDesktopsInputs = document.getElementById(
        "navigate_through_virtual_desktops_container"
      );
      navigateVirtualDesktopsInputs.style = "width: 100%";
      break;
    case "com.arkyasmal.windowactions.createvirtualdesktops":
      const createVirtualDesktopsInputs = document.getElementById(
        "create_virtual_desktop_inputs_container"
      );
      createVirtualDesktopsInputs.style = "width: 100%";
      break;
    case "com.arkyasmal.windowactions.movewindowsvirtual":
      const moveWindowsToVirtualDesktopInputs = document.getElementById(
        "move_windows_to_virtual_desktop"
      );
      moveWindowsToVirtualDesktopInputs.style = "width: 100%";
      wrapper.style = "";
      break;
    case "com.arkyasmal.windowactions.movewindowstomonitor":
      const moveWindowsToMonitorInputs = document.getElementById(
        "move_windows_to_monitor"
      );
      moveWindowsToMonitorInputs.style = "width: 100%";
      wrapper.style = "";
      break;
    case "com.arkyasmal.windowactions.movevirtualdesktopleft":
      break;
    case "com.arkyasmal.windowactions.movevirtualdesktopright":
      break;
    default:
      wrapper.style = "";
      break;
  }
};
const changeVirtualInputsDom = (value) => {
  if (!value) return;
  const moveWindowsVirtualDesktopNum = document.getElementById(
    "move_window_virtual_desktop_num"
  );
  const navigateVirtualDesktopNum = document.getElementById(
    "navigate_virtual_desktop_num"
  );
  const virtualDesktopsToCreate = document.getElementById(
    "virtual_desktops_to_create"
  );
  moveWindowsVirtualDesktopNum.value = value.newDesktop;
  navigateVirtualDesktopNum.value = value.newDesktop;
  virtualDesktopsToCreate.value = value.numOfDesktopsToCreate;
};
const onConnection = (jsn) => {
  /**
   * The passed 'applicationInfo' object contains various information about your
   * computer, Stream Deck version and OS-settings (e.g. colors as set in your
   * OSes display preferences.)
   * We use this to inject some dynamic CSS values (saved in 'common_pi.js'), to allow
   * drawing proper highlight-colors or progressbars.
   */

  console.log("connected");
  addDynamicStyles($SD.applicationInfo.colors, "connectSocket");
  console.log();
  /**
   * Current settings are passed in the JSON node
   * {actionInfo: {
   *      payload: {
   *          settings: {
   *                  yoursetting: yourvalue,
   *                  otherthings: othervalues
   * ...
   * To conveniently read those settings, we have a little utility to read
   * arbitrary values from a JSON object, eg:
   *
   * const foundObject = Utils.getProp(JSON-OBJECT, 'path.to.target', defaultValueIfNotFound)
   */
  determineContainerStyles(jsn.actionInfo.action);
  settings = Utils.getProp(jsn, "actionInfo.payload.settings", false);
  if (settings) {
    const { type, value, name } = settings;
    const winTypeInput = document.getElementById("select_win_type");
    const newType = type ? type : "program_name";
    winTypeInput.value = newType;
    saveSettings({ key: "type", value: winTypeInput.value });
    //send to plugin to populate active window list, and monitor list
    sendValueToPlugin("com.arkyasmal.windowActions.onActiveWindows", "action");
    sendValueToPlugin("com.arkyasmal.windowActions.onGetMonitorInfo", "action");
    //here for backwards support
    if (!value && name && typeof name === "string") {
      changeIdDom({ name: name });
    } else changeIdDom(value);
    changeResizeInputsDom(value ? value : {});
    changeVirtualInputsDom(value);
    updateUI(settings);
  }
};
