import { createOption } from './createOption';
type ActiveWindowType = {
  hWnd: string | number;
  pid: [number, number];
  program_name: string;
  title: string;
  win_class: string;
};

export const fetchActiveWindows = async (e?: Event) => {
  const streamDeckClient = SDPIComponents.streamDeckClient;
  await streamDeckClient.send('sendToPlugin', {
    action: 'com.arkyasmal.windowActions.onActiveWindows',
  });
};
/**
 * Setup window dropdown to fetch active windows
 */
export const configureActiveWindowDropdown = (id: string) => () => {
  const selectDropdown = document.getElementById(id) as HTMLSelectElement;
  //initial load
  fetchActiveWindows();
  // //refresh over time it's clicked
  if (!selectDropdown) return;
  selectDropdown.addEventListener('click', fetchActiveWindows);
};
const removeChildNodes = (el: HTMLSelectElement) => {
  if (!el) return;
  while (el.lastChild) {
    if (!el.lastChild) break;
    el.removeChild(el.lastChild);
  }
  return el;
};
export const populateActiveWindows =
  ({
    windowDropdownId,
    windowIdDropdownId,
  }: {
    windowDropdownId: string;
    windowIdDropdownId: string;
  }) =>
  async (res: PIEventRecievedEvent) => {
    const streamDeckClient = SDPIComponents.streamDeckClient;
    const { settings } = await streamDeckClient.getSettings();
    const { payload } = res;
    const result = payload.result as ActiveWindowType[];
    const selectDropdown = document.getElementById(
      windowDropdownId
    ) as HTMLSelectElement;
    const typeInput = (settings[windowIdDropdownId] ||
      'program_name') as keyof ActiveWindowType & 'win_title' & 'win_ititle';

    const options = result.map((window) => {
      console.log(window, typeInput);
      const value =
        typeInput === 'win_title' || typeInput === 'win_ititle'
          ? window.title
          : window[typeInput];
      const text = `${value} (${window.title})`;
      return createOption(value, text);
    });
    //replace old nodes, with new nodes
    removeChildNodes(selectDropdown);
    selectDropdown.append(...options);
  };
