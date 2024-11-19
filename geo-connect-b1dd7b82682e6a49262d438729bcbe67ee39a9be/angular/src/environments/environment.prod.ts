import { Environment } from '@abp/ng.core';

const baseUrl = 'http://localhost:4200';

export const environment = {
  production: true,
  application: {
    baseUrl,
    name: 'GeoConnect',
    logoUrl: '',
  },
  oAuthConfig: {
    issuer: 'https://localhost:44336',
    redirectUri: baseUrl,
    clientId: 'GeoConnect_App',
    responseType: 'code',
    scope: 'offline_access GeoConnect',
    requireHttps: true
  },
  apis: {
    default: {
      url: 'https://localhost:44336',
      rootNamespace: 'GeoConnect',
    },
  },
} as Environment;
