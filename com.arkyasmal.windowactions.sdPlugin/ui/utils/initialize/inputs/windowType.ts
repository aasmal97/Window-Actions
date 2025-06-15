import { WIN_ID_TYPE, WIN_ID_UI_TYPE } from '@/types/index';
type WindowIdTypeClassProps = {
  streamDeckClient: typeof SDPIComponents.streamDeckClient;
};
type WindowUIIdTypeClassProps = {
  streamDeckClient: typeof SDPIComponents.streamDeckClient;
};
/**
 * @description Use to configure the window type
 * and expose it to frontend code to dynamically set settings
 * and perform relevant logic
 */
export class WindowIdTypeClass {
  private client: typeof SDPIComponents.streamDeckClient;
  private onChangeSubscribedFns: ((
    inputType: WIN_ID_TYPE,
    oldInputType?: WIN_ID_TYPE
  ) => void)[] = [];
  public value: WIN_ID_TYPE = WIN_ID_TYPE.PROGRAM_NAME;
  constructor(props: WindowIdTypeClassProps) {
    if (!props.streamDeckClient) throw Error('No streamdeck client attached');
    this.client = props.streamDeckClient;
    this.client.getSettings().then((payload) => {
      const potentialValue =
        payload?.settings?.window_id_settings?.window_id_type ||
        payload.settings?.type;
      if (
        (Object.values(WIN_ID_TYPE) as string[]).includes(
          potentialValue as string
        )
      ) {
        this.value = potentialValue as WIN_ID_TYPE;
      } else this.setIdentifierType(WIN_ID_TYPE.PROGRAM_NAME);
    });
  }
  /**
   * @param e onchange event emitted from select/dropdown input
   * @description This is the function that is attach to the onchange handler
   */
  public onChange = (e: Event) => {
    const target = e.target as HTMLInputElement;
    const value = target.value as WIN_ID_TYPE;
    const oldValue = this.value;
    //save to settings & set internal value
    this.setIdentifierType(value);
    //update ui
    this.onChangeSubscribedFns.forEach((fn) => fn(value, oldValue));
  };
  /**
   * @param value value to set
   */
  public setIdentifierType(value: WIN_ID_TYPE) {
    if (!this.client) throw Error('No streamdeck client attached');
    this.value = value;
    this.setValueAsSetting(value);
  }
  public subscribeOnChange(
    fn: (newInputType: WIN_ID_TYPE, oldInputType?: WIN_ID_TYPE) => void
  ) {
    this.onChangeSubscribedFns.push(fn);
  }
  private setValueAsSetting = async (value: WIN_ID_TYPE) => {
    const settings = await this.client.getSettings();
    const newSettings = {
      ...(settings?.settings ?? {}),
      window_id_settings: {
        ...(settings?.settings?.window_id_settings ?? {}),
        window_id_type: value,
      },
    };
    this.client.setSettings(newSettings);
  };
}
/**
 * @description Use to configure the window type ui
 */
export class WindowIdUITypeClass {
  private client: typeof SDPIComponents.streamDeckClient;
  public value: WIN_ID_UI_TYPE = WIN_ID_UI_TYPE.TEXT;
  constructor(props: WindowUIIdTypeClassProps) {
    if (!props.streamDeckClient) throw Error('No streamdeck client attached');
    this.client = props.streamDeckClient;
  }
  /**
   * @param e onchange event emitted from select/dropdown input
   * @description This is the function that is attach to the onchange handler
   */
  public onChange = (e: Event) => {
    const target = e.target as HTMLInputElement;
    this.setUIType(target.value as WIN_ID_UI_TYPE);
  };
  /**
   * @param value value to set
   */
  public setUIType(value: WIN_ID_UI_TYPE) {
    if (!this.client) throw Error('No streamdeck client attached');
    this.value = value;
  }
  public detectWindowTypeChange(newValue: WIN_ID_TYPE, oldValue?: WIN_ID_TYPE) {
    if (!oldValue) return;
    const isNewValueTitle =
      newValue === WIN_ID_TYPE.WINDOW_TITLE ||
      newValue === WIN_ID_TYPE.WINDOW_PARTIAL_TITLE;
    const isOldValueTitle =
      oldValue === WIN_ID_TYPE.WINDOW_TITLE ||
      oldValue === WIN_ID_TYPE.WINDOW_PARTIAL_TITLE;
    const isTitle = isNewValueTitle && isOldValueTitle;
    if (!isTitle && newValue !== oldValue) {
      this.setUIType(WIN_ID_UI_TYPE.DROPDOWN);
    } else {
      this.setUIType(WIN_ID_UI_TYPE.TEXT);
    }
  }
}
