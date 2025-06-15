import path from 'path';
import { glob } from 'glob';
import CopyWebpackPlugin from 'copy-webpack-plugin';
import fs from 'fs';
import { environment } from './constants/general.constants';
import tsconfig from './tsconfig.json';
import { Configuration } from 'webpack';
import TsconfigPathsPlugin from 'tsconfig-paths-webpack-plugin';

const pluginName = 'com.arkyasmal.windowactions.sdPlugin' as const;
// Get all the action directories
const actionDirectories = glob.sync(`./${pluginName}/ui/*/`);
const entries = actionDirectories.reduce(
  (entry: Record<string, string>, dir) => {
    const actionName = path.basename(dir);
    const newPath = `./${dir}/index.ts`;
    const absolutePath = path.join(__dirname, newPath);
    if (!fs.existsSync(absolutePath)) return entry;
    entry[actionName] = newPath;
    return entry;
  },
  {}
);
const config: Configuration = {
  mode: environment,
  entry: entries,
  devtool: 'inline-source-map',
  output: {
    filename: '[name]/index.js',
    path: path.resolve(__dirname, `dist/${pluginName}/ui`),
    library: {
      name: 'WindowActions',
      type: 'global',
    },
  },
  resolve: {
    extensions: ['.ts', '.js'],
    plugins: [new TsconfigPathsPlugin({})],
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: tsconfig.exclude.map((dir) => path.resolve(__dirname, dir)),
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
        ...actionDirectories
          .filter((dir) => {
            return fs.existsSync(path.resolve(dir, 'index.html'));
          })
          .map((dir) => {
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
export default config;
