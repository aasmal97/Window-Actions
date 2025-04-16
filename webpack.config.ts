import path from 'path';
import { glob } from 'glob';
import CopyWebpackPlugin from 'copy-webpack-plugin';
import tsconfig from './tsconfig.json';
import fs from 'fs';
const pluginName = 'com.arkyasmal.windowactions.sdPlugin' as const;
// Get all the action directories
const actionDirectories = glob.sync(`./${pluginName}/ui/*/`);
const environment = (process.env.NODE_ENV || 'development').replace(
  / /g,
  ''
) as 'development' | 'production';
console.log(environment);
const entries = actionDirectories.reduce(
  (entry: Record<string, string>, dir) => {
    const actionName = path.basename(dir);
    const newPath = `${dir}/index.ts`;
    const absolutePath = path.join(__dirname, newPath);
    if (!fs.existsSync(absolutePath)) return entry;
    entry[actionName] = newPath;
    return entry;
  },
  {}
);
const watchOptions = {
  watch: true,
  watchOptions: {
    ignored: tsconfig.exclude,
    aggregateTimeout: 300,
  },
};
export default {
  ...(environment === 'development' ? watchOptions : {}),
  mode: environment,
  entry: entries,
  output: {
    filename: '[name]/index.js',
    path: path.resolve(__dirname, `dist/${pluginName}/ui`),
  },
  resolve: {
    extensions: ['.ts', '.js'],
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  plugins: [
    new CopyWebpackPlugin({
      patterns: [
        {
          from: path.resolve(__dirname, `${pluginName}/imgs`),
          to: path.resolve(__dirname, `dist/${pluginName}/imgs`),
        },
        {
          from: path.resolve(__dirname, `${pluginName}/manifest.json`),
          to: path.resolve(__dirname, `dist/${pluginName}/manifest.json`),
        },
        ...actionDirectories.map((dir) => {
          return {
            from: path.resolve(dir, 'index.html'),
            to: path.resolve(
              __dirname,
              `dist/${pluginName}/ui`,
              path.basename(dir),
              'index.html'
            ),
          };
        }),
      ],
    }),
  ],
};
