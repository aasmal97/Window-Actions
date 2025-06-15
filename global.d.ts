// global.d.ts
import { ActionSettingsPayload } from '@/types/index';
declare global {
  const SDPIComponents: {
    streamDeckClient: {
      getGlobalSettings(): Promise<Record<string, unknown>>;
      setGlobalSettings(value: unknown): void;
      didReceiveGlobalSettings: any;
      getSettings(): Promise<ActionSettingsPayload>;
      setSettings(value: ActionSettingsPayload['settings']): void;
      sendToPropertyInspector: any;
      send<T extends any>(event: T, payload?: unknown): Promise<void>;
      getConnectionInfo: () => any;
    };
  };
}
export {}; // Ensure this file is treated as a module
