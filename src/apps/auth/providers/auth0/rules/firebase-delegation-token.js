function (user, context, callback) {

  if (context.protocol === 'delegation' && context.request.body.api_type === 'firebase') {

    console.log('Beginning: Rule: Firebase Delegation Token: User Data:', user);

    // This is a firebase delegation call    
    // the key `firebase_data` needs to be spelled with this casing.
    user.firebase_data = {
      uid: user.app_metadata.hermes.user_id
    };

    console.log('Completed: Rule: Firebase Delegation Token: User Data:', user);
  }

  return callback(null, user, context);
}
