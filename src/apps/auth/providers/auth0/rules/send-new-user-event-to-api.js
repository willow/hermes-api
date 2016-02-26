function (user, context, callback) {

  function done() {
    callback(null, user, context);
  }

  if (context.protocol !== 'delegation') {
    // they are logging in, not renewing, refreshing, obtaining firebase token, etc.

    var appMetadata = user.app_metadata || {};
    appMetadata.hermes = appMetadata.hermes || {};

    if (!appMetadata.hermes.user_id) {
      // this is a new user
      var auth0UserId = user.user_id;
      console.log('Beginning: Rule: Send New User Event to API. User Id:', auth0UserId);

      var identity = {
        "email": user.email,
        "name": user.name,
        "nickname": user.nickname,
        "picture": user.picture,
        "meta": {"auth0": {"user_id": auth0UserId}}
      };

      var apiUrl = configuration.HERMES_API_DOMAIN;
      var postURL = "https://" + apiUrl + "/api/users/";
      var params = {
        "url": postURL,
        "json": identity
      };

      var f = function (err, response, body) {
        if (!err) {
          if (response.statusCode !== 201) {
            err = body;
          }
        }

        if (err) return callback(err);

        appMetadata.hermes.user_id = response.body.id;

        // persist the app_metadata update - https://auth0.com/docs/rules/metadata-in-rules#4
        auth0.users.updateAppMetadata(user.user_id, appMetadata)
            .then(function (newUser) { // get the most up-to-date data. newUser is the param: https://auth0.com/docs/rules/metadata-in-rules#4
              console.log('Completed: Rule: Send New User Event to API. User Id:', auth0UserId);
              // it's important to return newUser here in the callback. not exactly sure why, but when we don't do this
              // then other rules that run within auth0 won't have access to the app_metadata.
              return callback(null, newUser, context);
            }, callback);
      };

      request.post(params, f);
    } else {
      // not a new user

      done();

    }
  }
  else {
    // not an auth0 login call
    done();
  }
}
