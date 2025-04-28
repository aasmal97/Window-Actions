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
  //refresh over time it's clicked
  selectDropdown.addEventListener('click', fetchActiveWindows);
  // selectDropdown.addEventListener('change', (e) => {
  //     const value = (e.target as HTMLSelectElement).value;

  // });
};
const removeChildNodes = (el: HTMLSelectElement) => {
  while (el.hasChildNodes()) {
    if (el.lastChild === null) break;
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
  (res: PIEventRecievedEvent) => {
    const { payload } = res;
    const result = payload.result as ActiveWindowType[];
    const selectDropdown = document.getElementById(
      windowDropdownId
    ) as HTMLSelectElement;
    const winTypeInput = document.getElementById(
      windowIdDropdownId
    ) as HTMLOptionElement;
    const typeInput = winTypeInput.value as keyof ActiveWindowType &
      'win_title' &
      'win_ititle';
    const options = result.map((window) => {
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
