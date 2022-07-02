db.auth('admin', 'password')

db = db.getSiblingDB('video')

user = db.createUser({
  user: 'user',
  pwd: 'password',
  roles: [
    {
      role: 'readWrite',
      db: 'video',
    },
  ],
});
