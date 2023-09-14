mysql -h 127.0.0.1 -P 17010 -p main -u root -e "DROP DATABASE test; CREATE DATABASE test; DROP DATABASE main; CREATE DATABASE main;"
echo "Cleared databases main, test"