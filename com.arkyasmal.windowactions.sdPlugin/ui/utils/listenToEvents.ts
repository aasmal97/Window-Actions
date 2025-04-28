import { populateActiveWindows } from './configureActiveWindows';
import { windowDropdownId, windowIdDropdownId } from './constants';
export const listenToEvents = (event?: PIEventRecievedEvent | null) => {
  if (!event) return;
  const { payload } = event;
  const { action } = payload;
  switch (action) {
    case 'com.arkyasmal.windowActions.activeWindows':
      populateActiveWindows({
        windowDropdownId,
        windowIdDropdownId,
      })(event);
      break;
    case 'com.arkyasmal.windowActions.onGetMonitorInfo':
      break;
    default:
      return;
  }
};
