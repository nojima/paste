chmod a+w db
echo "CREATE TABLE Texts (id TEXT PRIMARY KEY, text TEXT NOT NULL);" | sqlite3 db/paste.sqlite3
chmod a+w db/paste.sqlite3
