import {
  listenToEvents,
  WindowIdTypeClass,
  WindowIdUITypeClass,
  WindowSelectedTextValueClass,
  WindowDropdownOptionsClass,
  windowDropdownElId,
} from '../utils';
const streamDeckClient = SDPIComponents.streamDeckClient;
/**
 * Configure window inputs for window dropdown
 */
export const WindowDropdownOptions = new WindowDropdownOptionsClass({
  streamDeckClient: streamDeckClient,
  dropdownElId: windowDropdownElId,
});
export const WindowSelectedTextValue = new WindowSelectedTextValueClass({
  streamDeckClient: streamDeckClient,
});
/**
 * Configure window inputs for window type inputs
 */
export const WindowIdType = new WindowIdTypeClass({
  streamDeckClient: streamDeckClient,
});
export const WindowIdUIType = new WindowIdUITypeClass({
  streamDeckClient: streamDeckClient,
});

const config = {
  WindowDropdownOptions: WindowDropdownOptions,
  WindowIdType: WindowIdType,
  WindowSelectedTextValue: WindowSelectedTextValue,
};
/**
 * Subscribe to changes in window type
 */
WindowIdType.subscribeOnChange(WindowDropdownOptions.changeOptionsByWinIdType);
WindowIdType.subscribeOnChange(WindowIdUIType.detectWindowTypeChange)
/**
 * Recieve events from plugin
 */
streamDeckClient.sendToPropertyInspector.subscribe(listenToEvents(config));
/**
 * Run initalization code when the DOM loads
 */
document.addEventListener('DOMContentLoaded', function () {
  //initalize options stored inside
  WindowDropdownOptions.replaceOptions();
});
