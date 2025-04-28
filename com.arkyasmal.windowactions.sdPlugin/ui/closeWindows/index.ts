import { configureActiveWindowDropdown } from "../utils/configureActiveWindows"
import { listenToEvents } from "../utils/listenToEvents";
const streamDeckClient = SDPIComponents.streamDeckClient;

/**
 * Configure all event listeners when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', async () => {
  configureActiveWindowDropdown("identifer_dropdown")();
});


/**
 * Recieve events from plugin
 */
streamDeckClient.sendToPropertyInspector.subscribe(listenToEvents);
