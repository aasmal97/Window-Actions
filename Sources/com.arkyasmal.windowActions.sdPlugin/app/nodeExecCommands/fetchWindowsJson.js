const path = require("path");
const fs = require("fs/promises");
const fetchWindowsJson = async (appDataDirectory) => {
  const dataDirectory = process.env.APPDATA;
  const filePath = path.join(
    dataDirectory,
    appDataDirectory,
    "activeWindows.json"
  );
  let promiseResolved;
  //grab json data
  const resolvePromise = async (interval, resolve) => {
    clearInterval(interval);
    resolve(promiseResolved);
    return promiseResolved;
  };
  const windowPromise = new Promise((resolve) => {
    setTimeout(async () => {
      const timeInterval = 500;
      const maxTimeToWait = timeInterval * 10;
      let elapsedTime = 0;
      const interval = setInterval(async () => {
        //immeaditely resolve and end interval timer
        if (promiseResolved) return resolvePromise(interval, resolve);
        //went over our threshold for waiting. end so we arent waiting forever
        if (elapsedTime > maxTimeToWait) {
          promiseResolved = [];
          return resolvePromise(interval, resolve);
        }
        try {
          const data = await fs.readFile(filePath);
          promiseResolved = JSON.parse(data);
          return resolvePromise(interval, resolve);
        } catch (e) {
          elapsedTime += timeInterval;
          console.error(e);
        }
      }, timeInterval);
    }, 1200);
  });

  //grab json data
  const result = await windowPromise;
  return result;
};
module.exports = fetchWindowsJson;
