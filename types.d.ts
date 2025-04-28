// global.d.ts
type ActionSettingsPayload = {
  coordinates?: {
    column: number;
    row: number;
  };
  isInMultiAction: boolean;
  settings: Record<string, unknown>;
};

declare global {
  const SDPIComponents: {
    streamDeckClient: {
      getGlobalSettings(): Promise<Record<string, unknown>>;
      setGlobalSettings(value: unknown): void;
      didReceiveGlobalSettings: any;
      getSettings(): Promise<ActionSettingsPayload>;
      setSettings(value: unknown): void;
      sendToPropertyInspector: any;
      send<T extends any>(event: T, payload?: unknown): Promise<void>;
      getConnectionInfo: () => any;
    };
  };
  type PIEventRecievedEvent = {
    action: string;
    context: string;
    event: string;
    payload: {
      action: string;
      result: unknown;
      targetContext: string;
    };
  };
  type PIEventSentSettings = {
    type: string;
    value: string | Record<string, unknown>;
    name: string;
  };
  type PIEventSendPayload = {
    action: string;
    context: string;
    event: string;
    payload: {
      action: string;
      settings: PIEventSentSettings;
    };
  };
}

export {}; // Ensure this file is treated as a module
