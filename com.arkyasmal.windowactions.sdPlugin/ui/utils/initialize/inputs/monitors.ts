import { MonitorType } from '@/types/index';
type DisplayMonitorTypeClassProps = {
  streamDeckClient: typeof SDPIComponents.streamDeckClient;
};
type MonitorValue = {
  monitor_name: string;
  monitor_idx: number;
};
export class MonitorDisplayValue {
  private client: typeof SDPIComponents.streamDeckClient | null = null;
  private monitorData: MonitorType[] = [];
  public value: MonitorValue | null = null; // value of the monitor
  constructor(props: DisplayMonitorTypeClassProps) {
    if (!props.streamDeckClient) throw Error('No streamdeck client attached');
    this.client = props.streamDeckClient;
    this.client.getSettings().then((settings) => {
      const potentialValue =
        (settings?.settings?.monitor_settings?.monitor_idx &&
          typeof settings?.settings?.monitor_settings?.monitor_idx !==
            'number') ||
        (settings.settings?.value?.newMonitor as number | null);
      const monitorName =
        settings?.settings?.monitor_settings?.monitor_name ||
        `Generic PnP Monitor`;
      if (!potentialValue)
        this.value = {
          monitor_idx: potentialValue || 0,
          monitor_name: monitorName,
        };
      else this.setMonitorValue(null);
    });
  }
  onChange = (e: Event) => {
    const target = e.target as HTMLInputElement;
    if (!target.value) return;
    const monitorIdx = parseInt(target.value) || 0;
    if (monitorIdx >= this.monitorData.length - 1) return;
    const currMonitor = this.monitorData.find(
      (monitor) => monitor.idx === monitorIdx
    );
    if (!currMonitor) return this.setMonitorValue(null);
    this.setMonitorValue({
      monitor_name: currMonitor.name,
      monitor_idx: currMonitor.idx,
    });
  };
  private async setMonitorValue(value: MonitorValue | null) {
    if (!this.client) throw Error('No streamdeck client attached');
    this.value = value;
    const settings = await this.client.getSettings();
    const newSettings = {
      ...(settings?.settings ?? {}),
      monitor_settings: {
        ...(settings?.settings?.monitor_settings ?? {}),
      },
    };
    this.client.setSettings(newSettings);
  }
}
