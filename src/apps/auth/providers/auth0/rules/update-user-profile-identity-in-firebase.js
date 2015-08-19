function (user, context, callback) {

  if (context.protocol !== 'delegation') { // they are logging in, not renewing, refreshing, obtaining firebase token, etc.

    var callFirebase = function () {
      var fbId = user.app_metadata.hermes.userId;

      var fbIdentity = {
        // remember, firebase keys can be urls, make them dash-case
        "email": user.email,
        "name": user.name,
        "nickname": user.nickname,
        "picture": user.picture
      };

      var putURL = baseURL + "/users/" + fbId + "/identity.json?auth=" + secret;
      request.put({
            "url": putURL,
            "json": fbIdentity
          },

          function (err, response, body) {
            if (!err) {
              if (response.statusCode !== 200) {
                err = body;
              }
            }

            if (err) return callback(err);
            return callback(null, user, context);
          });
    };

    var promise = require('promise');

    var baseURL = configuration.FIREBASE_URL;
    var secret = configuration.FIREBASE_SECRET;

    var appMetadata = user.app_metadata || {};
    appMetadata.hermes = appMetadata.hermes || {};

    if (!appMetadata.hermes.userId) {
      console.log('Rule: Update User Profile Identity in Firebase: Hermes userId not found');
      console.log('Rule: Update User Profile Identity in Firebase: Auth0 user_id:', user.user_id);

      var randomize = require('randomatic');

      appMetadata.hermes.userId = randomize('aA0', 6);

      // persist the app_metadata update - https://auth0.com/docs/rules/metadata-in-rules#4
      auth0.users.updateAppMetadata(user.user_id, appMetadata)
          .then(function (newUser) {
            user = newUser; // get the most up-to-date data. newUser is the param: https://auth0.com/docs/rules/metadata-in-rules#4
            callFirebase();
          }, callback);

    } else {
      console.log('Rule: Update User Profile Identity in Firebase: Hermes userId was found');
      callFirebase();
    }

    console.log('Rule: Update User Profile Identity in Firebase: User', user);
    console.log('Rule: Update User Profile Identity in Firebase: Context', context);
  } else {
    // not an auth0 login call
    callback(null, user, context);
  }
}
