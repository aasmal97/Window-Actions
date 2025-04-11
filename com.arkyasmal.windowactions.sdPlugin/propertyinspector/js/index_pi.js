/* global addDynamicStyles, $SD, Utils */
/* eslint-disable no-extra-boolean-cast */
/* eslint-disable no-else-return */

/**
 * This example contains a working Property Inspector, which already communicates
 * with the corresponding plugin throug settings and/or direct messages.
 * If you want to use other control-types, we recommend copy/paste these from the
 * PISamples demo-library, which already contains quite some example DOM elements
 */

/**
 * First we declare a global variable, which change all elements behaviour
 * globally. It installs the 'onchange' or 'oninput' event on the HTML controls and fiels.
 *
 * Change this, if you want interactive elements act on any modification (oninput),
 * or while their value changes 'onchange'.
 */
var onchangeevt = "onchange"; // 'oninput';

/**
 * cache the static SDPI-WRAPPER, which contains all your HTML elements.
 * Please make sure, you put all HTML-elemenets into this wrapper, so they
 * are drawn properly using the integrated CSS.
 */

let sdpiWrapper = document.querySelector(".sdpi-wrapper");

/**
 * Since the Property Inspector is instantiated every time you select a key
 * in Stream Deck software, we can savely cache our settings in a global variable.
 */

let settings;
/**
 * This is a quick and simple way to localize elements and labels in the Property
 * Inspector's UI without touching their values.
 * It uses a quick 'lox()' function, which reads the strings from a global
 * variable 'localizedStrings' (in 'common.js')
 */

// eslint-disable-next-line no-unused-vars
function localizeUI() {
  const el = document.querySelector(".sdpi-wrapper") || document;
  let t;
  Array.from(el.querySelectorAll("sdpi-item-label")).forEach((e) => {
    t = e.textContent.lox();
    if (e !== t) {
      e.innerHTML = e.innerHTML.replace(e.textContent, t);
    }
  });
  Array.from(el.querySelectorAll("*:not(script)")).forEach((e) => {
    if (
      e.childNodes &&
      e.childNodes.length > 0 &&
      e.childNodes[0].nodeValue &&
      typeof e.childNodes[0].nodeValue === "string"
    ) {
      t = e.childNodes[0].nodeValue.lox();
      if (e.childNodes[0].nodeValue !== t) {
        e.childNodes[0].nodeValue = t;
      }
    }
  });
}

function saveSettings(sdpi_collection) {
  if (typeof sdpi_collection !== "object") return;

  if (sdpi_collection.hasOwnProperty("key") && sdpi_collection.key != "") {
    if (sdpi_collection.value && sdpi_collection.value !== undefined) {
      console.log(sdpi_collection.key, " => ", sdpi_collection.value);
      settings[sdpi_collection.key] = sdpi_collection.value;
      console.log("setSettings....", settings);
      $SD.api.setSettings($SD.uuid, settings);
    }
  }
}
/**
 * 'sendValueToPlugin' is a wrapper to send some values to the plugin
 *
 * It is called with a value and the name of a property:
 *
 * sendValueToPlugin(<any value>), 'key-property')
 *
 * where 'key-property' is the property you listen for in your plugin's
 * 'sendToPlugin' events payload.
 *
 */

function sendValueToPlugin(value, prop, sameActionBtn = false) {
  if ($SD.connection && $SD.connection.readyState === 1) {
    const json = {
      action: $SD.actionInfo["action"],
      event: "sendToPlugin",
      context: $SD.uuid,
      payload: {
        [prop]: value,
        targetContext: $SD.actionInfo["context"],
      },
    };
    if (sameActionBtn) json.payload.action = $SD.actionInfo["action"];
    $SD.connection.send(JSON.stringify(json));
  }
}

const updateUI = (pl) => {
  console.log(pl);
  // console.log(pl)
  // Object.keys(pl).map((e) => {
  //   if (e && e != "") {
  //     const foundElement = document.querySelector(`#${e}`);
  //     console.log(`searching for: #${e}`, "found:", foundElement);
  //     if (foundElement && foundElement.type !== "file") {
  //       foundElement.value = pl[e];
  //       const maxl = foundElement.getAttribute("maxlength") || 50;
  //       const labels = document.querySelectorAll(`[for='${foundElement.id}']`);
  //       if (labels.length) {
  //         for (let x of labels) {
  //           x.textContent = maxl
  //             ? `${foundElement.value.length}/${maxl}`
  //             : `${foundElement.value.length}`;
  //         }
  //       }
  //     }
  //   }
  // });
};

/**
 * Something in the PI changed:
 * either you clicked a button, dragged a slider or entered some text
 *
 * The 'piDataChanged' event is sent, if data-changes are detected.
 * The changed data are collected in a JSON structure
 *
 * It looks like this:
 *
 *  {
 *      checked: false
 *      group: false
 *      index: 0
 *      key: "mynameinput"
 *      selection: []
 *      value: "Elgato"
 *  }
 *
 * If you set an 'id' to an input-element, this will get the 'key' of this object.
 * The input's value will get the value.
 * There are other fields (e.g.
 *      - 'checked' if you clicked a checkbox
 *      - 'index', if you clicked an element within a group of other elements
 *      - 'selection', if the element allows multiple-selections
 * )
 *
 * Please note:
 * the template creates this object for the most common HTML input-controls.
 * This is a convenient way to start interacting with your plugin quickly.
 *
 */

const onPIDataChange = (returnValue) => {
  console.log(
    "%c%s",
    "color: white; background: blue}; font-size: 15px;",
    "piDataChanged"
  );
  console.log(returnValue);

  if (returnValue.key === "clickme") {
    postMessage = (w) => {
      w.postMessage(
        Object.assign({}, $SD.applicationInfo.application, {
          action: $SD.actionInfo.action,
        }),
        "*"
      );
    };

    if (!window.xtWindow || window.xtWindow.closed) {
      window.xtWindow = window.open(
        "../externalWindow.html",
        "External Window"
      );
      setTimeout(() => postMessage(window.xtWindow), 200);
    } else {
      postMessage(window.xtWindow);
    }
  } else {
    /* SAVE THE VALUE TO SETTINGS */
    saveSettings(returnValue);

    /* SEND THE VALUES TO PLUGIN */
    sendValueToPlugin(returnValue, "sdpi_collection");
  }
};
$SD.on("connected", onConnection);

/**
 * The 'sendToPropertyInspector' event can be used to send messages directly from your plugin
 * to the Property Inspector without saving these messages to the settings.
 */
$SD.on("sendToPropertyInspector", respondToEvents);

$SD.on("piDataChanged", onPIDataChange);


document.addEventListener("DOMContentLoaded", function () {
  document.body.classList.add(
    navigator.userAgent.includes("Mac") ? "mac" : "win"
  );
  // prepareDOMElements();
  $SD.on("localizationLoaded", (language) => {
    localizeUI();
  });
});

/** the beforeunload event is fired, right before the PI will remove all nodes */
window.addEventListener("beforeunload", function (e) {
  e.preventDefault();
  sendValueToPlugin("propertyInspectorWillDisappear", "property_inspector");
  // Don't set a returnValue to the event, otherwise Chromium with throw an error.  // e.returnValue = '';
});

function gotCallbackFromWindow(parameter) {
  console.log(parameter);
}
