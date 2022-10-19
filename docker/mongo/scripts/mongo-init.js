function getEnvVariable(envVar, defaultValue) {
    var command = run("sh", "-c", `printenv --null ${envVar} >/tmp/${envVar}.txt`);
    if (command != 0) return defaultValue;
    return cat(`/tmp/${envVar}.txt`)
}

var dbUser = getEnvVariable('SQL_USER', 'app_user');
var dbPwd = getEnvVariable('SQL_PASSWORD', 'app_user()');
var dbName = getEnvVariable('SQL_DATABASE', 'ShortenedUrls');
var dbCollectionName = getEnvVariable('DB_COLLECTION_NAME', 'Urls');
db = db.getSiblingDB(dbName);
db.createUser({
    'user': dbUser,
    'pwd': dbPwd,
    'roles': [
        {
            'role': 'dbOwner',
            'db': getEnvVariable('DB_NAME', 'MeanUrls')
        }
    ]
});

db.createCollection(dbCollectionName);
