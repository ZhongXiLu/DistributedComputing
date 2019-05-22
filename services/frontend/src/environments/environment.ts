// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const proxy = {
    url: 'http://192.168.99.100'
};

export const environment = {
  production: false,

  // for docker-compose
  userServiceUrl: 'http://localhost:5001',
  postServiceUrl: 'http://localhost:5002',
  followServiceUrl: 'http://localhost:5011',
  notificationServiceUrl: 'http://localhost:5010',
  tagServiceUrl: 'http://localhost:5003',
  authServiceUrl: 'http://localhost:5004',
  likeServiceUrl: 'http://localhost:5005',
  commentServiceUrl: 'http://localhost:5006',
  messageServiceUrl: 'http://localhost:5013',
  friendServiceUrl: 'http://localhost:5012',
  newsfeedServiceUrl: 'http://localhost:5007',
  antiCyberbullyingServiceUrl: 'http://localhost:5008',
  adServiceUrl: 'http://localhost:5009'

  // for kubernetes
  // userServiceUrl: proxy.url + ':30026',
  // postServiceUrl: proxy.url + ':30022',
  // followServiceUrl: proxy.url + ':30010',
  // notificationServiceUrl: proxy.url + ':30018',
  // tagServiceUrl: proxy.url + ':30024',
  // authServiceUrl: proxy.url + ':30005',
  // likeServiceUrl: proxy.url + ':30013',
  // commentServiceUrl: proxy.url + ':30008',
  // messageServiceUrl: proxy.url + ':30016',
  // friendServiceUrl: proxy.url + ':30012',
  // newsfeedServiceUrl: proxy.url + ':30017',
  // antiCyberbullyingServiceUrl: proxy.url + ':30003',
  // adServiceUrl: proxy.url + ':30001'
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.
