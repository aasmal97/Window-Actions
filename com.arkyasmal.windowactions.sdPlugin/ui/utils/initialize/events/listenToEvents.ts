import { WindowDropdownOptionsClass } from '../inputs/windowIdValue';
import { WindowIdTypeClass, WindowSelectedTextValueClass } from '../inputs';
import { PIEventRecievedEvent } from '@/types/index';
/**
 * @description The config objects that takes in all
 * inputs/classes that listen to events from the plugin
 */
type ListenToEventConfig = {
  WindowDropdownOptions: WindowDropdownOptionsClass;
  WindowIdType: WindowIdTypeClass;
  WindowSelectedTextValue: WindowSelectedTextValueClass;
};

export const listenToEvents =
  (config: ListenToEventConfig) => (event?: PIEventRecievedEvent | null) => {
    const { WindowDropdownOptions } = config;
    if (!event) return;
    const { payload } = event;
    const { action } = payload;
    switch (action) {
      case 'com.arkyasmal.windowActions.activeWindows':
        WindowDropdownOptions.recieveActiveWindowsEvent(payload);
        break;
      case 'com.arkyasmal.windowActions.onGetMonitorInfo':
        break;
      default:
        return;
    }
  };
