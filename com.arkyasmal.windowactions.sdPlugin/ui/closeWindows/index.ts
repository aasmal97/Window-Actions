const streamDeckClient = SDPIComponents.streamDeckClient;
export const fetchActiveWindows = async (e: Event) => {
  await streamDeckClient.send('sendToPlugin', {
    action: 'com.arkyasmal.windowActions.onActiveWindows',
  });
};
/**
 * Setup window dropdown to fetch active windows
 */
const configureActiveWindowDropdown = () => {
  const selectDropdown = document.getElementById(
    'identifer_dropdown'
  ) as HTMLSelectElement;
  selectDropdown.addEventListener('load', fetchActiveWindows);
  selectDropdown.addEventListener('click', fetchActiveWindows);
};

/**
 * Configure all event listeners when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', async () => {
    configureActiveWindowDropdown();
    const info = await streamDeckClient.getConnectionInfo();
    console.log(info)
});

const listenToEvents = (
  event?: Record<string, string | Record<string, string>> | null
) => {
    console.log(event)
};
/**
 * Recieve events from plugin
 */
streamDeckClient.sendToPropertyInspector.subscribe(listenToEvents);
