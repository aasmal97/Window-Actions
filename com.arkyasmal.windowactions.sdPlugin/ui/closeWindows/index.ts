import { configureActiveWindowDropdown } from '../utils/configureActiveWindows';
import { listenToEvents } from '../utils/listenToEvents';
import { windowDropdownId } from '../utils/constants';
const streamDeckClient = SDPIComponents.streamDeckClient;

/**
 * Configure all event listeners when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', async () => {
  configureActiveWindowDropdown(windowDropdownId)();
});

/**
 * Recieve events from plugin
 */
streamDeckClient.sendToPropertyInspector.subscribe(listenToEvents);
