import {
  ActiveWindowPayload,
  ActiveWindowType,
  WIN_ID_TYPE,
  WIN_ID_UI_TYPE,
} from '@/types/pluginEvents';
import { createOption, removeAllOptions } from '../..';

type WindowDropdownOptionsProps = {
  streamDeckClient: typeof SDPIComponents.streamDeckClient;
  dropdownElId: string;
};
type WindowSelectedTextValueProps = {
  streamDeckClient: typeof SDPIComponents.streamDeckClient;
};
export class WindowDropdownOptionsClass {
  private client: typeof SDPIComponents.streamDeckClient;
  private dropdownElId: string;
  public activeWindowData: ActiveWindowType[] = [];
  public options: HTMLOptionElement[] = [];
  public selectedValue: string | null = null;
  constructor(props: WindowDropdownOptionsProps) {
    if (!props.streamDeckClient) throw Error('No streamdeck client attached');
    this.client = props.streamDeckClient;
    this.dropdownElId = props.dropdownElId;
    this.fetchActiveWindows();
  }
  /**
   * @param e - Any event from a handler
   * @description - SENDS a websocket event to the streamdeck plugin
   * to initiate a fetch of active windows. This function is meant
   * to be attached to an event handler like `onload`, or whenever
   * initalization of windows is required
   */
  public fetchActiveWindows = async (e?: Event) => {
    await this.client.send('sendToPlugin', {
      action: 'com.arkyasmal.windowActions.onActiveWindows',
    });
  };
  /**
   * The following functions are mean to handle RECIEVING a websocket
   * event from the streamdeck plugin, and make changes accordingly
   */
  public recieveActiveWindowsEvent = async (res: ActiveWindowPayload) => {
    const { settings } = await this.client.getSettings();
    const result = res?.result?.windows;
    const currType =
      settings?.window_id_settings?.window_id_type ||
      settings?.type ||
      WIN_ID_TYPE.PROGRAM_NAME;
    //only populate if new options exist
    if (!result) return;
    //populate new options data
    this.activeWindowData = result;
    this.options = result.map((window) => {
      const value =
        currType === WIN_ID_TYPE.WINDOW_TITLE ||
        currType === WIN_ID_TYPE.WINDOW_PARTIAL_TITLE
          ? window.title
          : window[currType];
      const text = `${value} (${window.title})`;
      return createOption(value, text);
    });
    this.replaceOptions(this.options);
  };
  /**
   * add options to dropdown
   */
  public replaceOptions = (options?: HTMLOptionElement[]) => {
    options = options || this.options;
    const selectDropdown = document.getElementById(
      this.dropdownElId
    ) as HTMLSelectElement;
    //this means it hasn't loaded into the dom yet
    if (!selectDropdown) return;
    //replace old nodes, with new nodes
    removeAllOptions(selectDropdown);
    selectDropdown.append(...options);
  };
  public changeOptionsByWinIdType = (typeInput: WIN_ID_TYPE) => {
    //never calculate on empty data
    if (!this.activeWindowData || this.activeWindowData.length <= 0) return;
    //change ids according to change win type
    this.options = this.activeWindowData.map((window) => {
      const value =
        typeInput === WIN_ID_TYPE.WINDOW_TITLE ||
        typeInput === WIN_ID_TYPE.WINDOW_PARTIAL_TITLE
          ? window.title
          : window[typeInput];
      const text = `${value} (${window.title})`;
      return createOption(value, text);
    });
    this.replaceOptions(this.options);
  };
}
/**
 * @description Use to configure the window id value.
 * If the type is set to WIN_ID_TYPE.WINDOW_TITLE, then this
 * will be the window title, and so forth
 */
export class WindowSelectedTextValueClass {
  private client: typeof SDPIComponents.streamDeckClient;
  public value: string | number | null = null;
  constructor(props: WindowSelectedTextValueProps) {
    if (!props.streamDeckClient) throw Error('No streamdeck client attached');
    this.client = props.streamDeckClient;
    this.client.getSettings().then((payload) => {
      const potentialValue =
        //new support
        payload?.settings?.window_id_settings?.window_id_text_value ||
        //legacy support
        payload?.settings?.value?.name ||
        payload?.settings?.name;
      if (!potentialValue) this.value = potentialValue as string;
      else this.setWindowIdValue(null);
    });
  }
  /**
   * @param e onchange event emitted from select/dropdown input
   * @description This is the function that is attach to the onchange handler
   */
  public onChange = (e: Event) => {
    const target = e.target as HTMLInputElement;
    this.setWindowIdValue(target.value as WIN_ID_UI_TYPE);
  };
  /**
   * @param value value to set
   */
  public setWindowIdValue(value: string | null) {
    if (!this.client) throw Error('No streamdeck client attached');
    this.value = value;
    this.setValueAsSetting(value);
  }
  private setValueAsSetting = async (value: string | null) => {
    const settings = await this.client.getSettings();
    const newSettings = {
      ...(settings?.settings ?? {}),
      window_id_settings: {
        ...(settings?.settings?.window_id_settings ?? {}),
        window_id_text_value: value,
      },
    };
    this.client.setSettings(newSettings);
  };
}
