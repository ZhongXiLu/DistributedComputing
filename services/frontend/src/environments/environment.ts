// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const proxy = {
    url: 'http://localhost:8001/api/v1/namespaces/default/services/'
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
  // userServiceUrl: proxy.url + 'users:5000/proxy',
  // postServiceUrl: proxy.url + 'post:5000/proxy',
  // followServiceUrl: proxy.url + 'follow:5000/proxy',
  // notificationServiceUrl: proxy.url + 'notification:5000/proxy',
  // tagServiceUrl: proxy.url + 'tag:5000/proxy',
  // authServiceUrl: proxy.url + 'authentication:5000/proxy',
  // likeServiceUrl: proxy.url + 'like:5000/proxy',
  // commentServiceUrl: proxy.url + 'comment:5000/proxy',
  // messageServiceUrl: proxy.url + 'message:5000/proxy',
  // friendServiceUrl: proxy.url + 'friend:5000/proxy',
  // newsfeedServiceUrl: proxy.url + 'newsfeed:5000/proxy',
  // antiCyberbullyingServiceUrl: proxy.url + 'anti-cyberbullying:5000/proxy',
  // adServiceUrl: proxy.url + 'ad:5000/proxy'
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.
