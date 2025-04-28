export const listenToEvents = (event?: PIEventRecievedEvent | null) => {
  if (!event) return;
  const { payload } = event;
  const { action } = payload;
  switch (action) {
    case 'com.arkyasmal.windowActions.onActiveWindows':
      break;
    case 'com.arkyasmal.windowActions.onGetMonitorInfo':
      break;
    default:
      return;
  }
};
