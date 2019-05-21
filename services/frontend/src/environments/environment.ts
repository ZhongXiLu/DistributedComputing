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
  // userServiceUrl: proxy.url + 'users/proxy',
  // postServiceUrl: proxy.url + 'post/proxy',
  // followServiceUrl: proxy.url + 'follow/proxy',
  // notificationServiceUrl: proxy.url + 'notification/proxy',
  // tagServiceUrl: proxy.url + 'tag/proxy',
  // authServiceUrl: proxy.url + 'authentication/proxy',
  // likeServiceUrl: proxy.url + 'like/proxy',
  // commentServiceUrl: proxy.url + 'comment/proxy',
  // messageServiceUrl: proxy.url + 'message/proxy',
  // friendServiceUrl: proxy.url + 'friend/proxy',
  // newsfeedServiceUrl: proxy.url + 'newsfeed/proxy',
  // antiCyberbullyingServiceUrl: proxy.url + 'anti-cyberbullying/proxy',
  // adServiceUrl: proxy.url + 'ad/proxy'
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.
