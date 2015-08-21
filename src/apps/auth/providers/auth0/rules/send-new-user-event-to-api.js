function (user, context, callback) {

  function done() {
    callback(null, user, context);
  }

  if (context.protocol !== 'delegation') {
    // they are logging in, not renewing, refreshing, obtaining firebase token, etc.

    if (!user.signed_up) {
      // this is a new user
      var userId = user.user_id;
      console.log('Beginning: Rule: Send New User Event to API. User Id:', userId);

      var identity = {
        "user_email": user.email,
        "user_name": user.name,
        "user_nickname": user.nickname,
        "user_picture": user.picture,
        "user_attrs": {"auth0": {"user_id": userId}}
      };

      var postURL = "https://hermes-api-qa.herokuapp.com/api/users/";
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

        // `signed_up` will be persisted into app_metadata.
        // it's probably better to explicitly state this. consider a use case the initial sign up process takes > 1 minute (background processing, imports).
        // multiple attempts to sign in during this time frame should not result in extra api calls, indicating new sign ups. if they did try to sign in
        // they'd get errors anyway (api, unique constraints). really, they should see the sign up process indicator and receive no errors.
        user.persistent.signed_up = true;

        console.log('Completed: Rule: Send New User Event to API. User Id:', userId);
        return callback(null, user, context);
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
