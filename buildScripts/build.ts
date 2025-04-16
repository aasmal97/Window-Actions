import fs from 'fs';
import path from 'path';
import child_process from 'child_process';
import webpack from 'webpack';
import webpackConfig from '../webpack.config';
const compiler = webpack(webpackConfig);
function findPackageJson(directory: string | null): string | null {
  if (!directory) {
    return null;
  }
  const parent = path.dirname(directory);
  const files = fs.readdirSync(directory);
  if (files.includes('package.json')) {
    return directory;
  } else {
    return findPackageJson(parent);
  }
}

function installRequirements(): void {
  const currentDir = __dirname;
  const rootPath = findPackageJson(currentDir);
  if (!rootPath) return;
  child_process.execSync('pip install -r requirements.txt', {
    cwd: rootPath,
    stdio: 'inherit'
  });
}

function compileApp(): void {
  const currentDir = __dirname;
  const rootPath = findPackageJson(currentDir);
  if (!rootPath) return;
  const setupLocation = path.normalize(
    path.join(rootPath, `buildScripts`, 'setup.py')
  );
  // compile python to executable
  child_process.execSync(`py "${setupLocation}" build`, {
    cwd: rootPath,
    stdio: 'inherit',
  });
  //compile webpack app
  compiler.run((err, stats) => {
    if (err) {
      console.error(err);
      return;
    }
    if (!stats) return;
    console.log(
      stats.toString({
        chunks: false,
        colors: true,
      })
    );
  });
}

(function main() {
  installRequirements();
  compileApp();
})();

// const appPath = path.join(
//   os.homedir(),
//   'AppData',
//   'Roaming',
//   'Elgato',
//   'StreamDeck',
//   'Plugins',
//   pluginName
// );

// const buildPath = path.normalize(path.resolve(currentDir, '..\\Build'));
// const releasePath = path.normalize(path.resolve(currentDir, '..\\Release'));
// const buildPluginPath = path.join(buildPath, pluginName);
// const sourcePluginPath = path.normalize(
//   path.resolve(currentDir, '..\\Sources', pluginName)
// );
// const releasePluginPath = path.join(
//   releasePath,
//   `${shortPluginName}.streamDeckPlugin`
// );
