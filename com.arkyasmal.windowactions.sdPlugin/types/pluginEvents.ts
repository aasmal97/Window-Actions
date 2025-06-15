export enum WIN_ID_TYPE {
  PROGRAM_NAME = 'program_name',
  WINDOW_TITLE = 'win_title',
  WINDOW_PARTIAL_TITLE = 'win_ititle',
  WINDOW_HWND = 'hWnd',
  WINDOW_CLASS = 'win_class',
}
export enum WIN_ID_UI_TYPE {
  DROPDOWN = 'dropdown',
  TEXT = 'text',
}
export enum SUB_ACTION_TYPE {
  ACTIVE_WINDOWS = 'com.arkyasmal.windowActions.activeWindows',
  CURRENT_MONITORS = 'com.arkyasmal.windowActions.onGetMonitorInfo',
}
export type ActiveWindowType = {
  hWnd: string | number;
  pid: [number, number];
  program_name: string;
  title: string;
  win_class: string;
};
export type ActiveWindowPayload = {
  action: SUB_ACTION_TYPE.ACTIVE_WINDOWS;
  result: {
    windows: ActiveWindowType[];
  };
  targetContext: string;
  settings?: Record<string, unknown>;
};
export type MonitorType = {
  name: string;
  idx: number;
  instance_name?: string | null;
  man_name?: string | null;
  code?: string | number | null;
  user_name?: string | number | null;
};
export type CurrentMonitorPayload = {
  action: SUB_ACTION_TYPE.CURRENT_MONITORS;
  result: {
    monitors: MonitorType[];
  };
  targetContext: string;
  settings?: Record<string, unknown>;
};
export type SubEventPayload = ActiveWindowPayload | CurrentMonitorPayload;
export type PIEventRecievedEvent = {
  action: string;
  context: string;
  event: string;
  device: string;
  payload: SubEventPayload;
};
export type PIEventSentSettings = {
  type: string;
  value: string | Record<string, unknown>;
  name: string;
};
export type PIEventSendPayload = {
  action: string;
  context: string;
  event: string;
  payload: {
    action: string;
    settings: PIEventSentSettings;
  };
};
export type ActionSettingsPayload = {
  coordinates?: {
    column: number;
    row: number;
  };
  isInMultiAction: boolean;
  settings?: {
    window_id_settings?: {
      window_id_type?: WIN_ID_TYPE;
      window_id_text_value?: string | null;
    };
    monitor_settings?: {
      monitor_name?: string | null;
      monitor_idx?: number | null;
    };
    //legacy
    value?: Record<string, unknown>;
    name?: string;
    type?: WIN_ID_TYPE;
  };
};
