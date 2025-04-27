import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import webpack from 'webpack';
import type { Configuration } from 'webpack';
import webpackConfig from '../webpack.config';
import tsconfig from '../tsconfig.json';
import { environment, pluginName } from '../constants/general.constants';
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
  execSync('pip install -r requirements.txt', {
    cwd: rootPath,
    stdio: 'inherit',
  });
}
const compileWebpackApp = (rootPath: string) =>
  //compile webpack app for production
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
    if (stats.hasErrors()) console.error('Compilation failed.');
    // validate plugin
    execSync(`npx streamdeck validate ./dist/${pluginName}`, {
      cwd: rootPath,
      stdio: 'inherit',
    });
    // pack plugin
    execSync(`npx streamdeck pack ./dist/${pluginName} --output Release`, {
      cwd: rootPath,
      stdio: 'inherit',
    });
  });
const watchWebpackApp = (rootPath: string) => {
  //watch if development mode
  const watchOptions: Configuration['watchOptions'] = {
    ignored: tsconfig.exclude,
    aggregateTimeout: 300,
  };
  console.log('Compiling...');
  // link plugin to streamdeck folder
  execSync(`npx streamdeck link ./dist/${pluginName}`, {
    cwd: rootPath,
    stdio: 'inherit',
  });
  console.log('Watching for changes...');
  compiler.watch(watchOptions, (err, stats) => {
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
};
function compileApp(): void {
  const currentDir = __dirname;
  const rootPath = findPackageJson(currentDir);
  if (!rootPath) return;
  const setupLocation = path.normalize(
    // path.join(rootPath, `buildScripts`, 'setup.py')
    path.join(
      rootPath,
      pluginName,
      'app',
      'scripts',
      'setup.py'
    )
  );
  // compile python to executable
  execSync(`py "${setupLocation}" build`, {
    cwd: rootPath,
    stdio: 'inherit',
  });

  //watch if development mode
  if (environment === 'development') {
    watchWebpackApp(rootPath);
  } else {
    //compile webpack app for production
    compileWebpackApp(rootPath);
  }
}

(function main() {
  installRequirements();
  compileApp();
})();
