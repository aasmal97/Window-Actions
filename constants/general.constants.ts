export const shortPluginName = 'com.arkyasmal.windowactions' as const;
export const extension = 'sdPlugin';
export const pluginName = `${shortPluginName}.${extension}` as const;
export const environment = (process.env.NODE_ENV || 'development').replace(
  / /g,
  ''
) as 'development' | 'production';