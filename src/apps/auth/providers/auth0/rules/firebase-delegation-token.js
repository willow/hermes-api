function (user, context, callback) {

  if (context.protocol === 'delegation' && context.request.body.api_type === 'firebase') {

    // This is a firebase delegation call    
    // the key `firebase_data` needs to be spelled with this casing.
    user.firebase_data = {
      uid: user.app_metadata.hermes.user_id
    };

    console.log('Rule: Firebase Delegation Token: User Data:', user);
  }

  return callback(null, user, context);
}
