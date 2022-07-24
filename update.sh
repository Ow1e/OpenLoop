echo "Welcome to the OpenLoop Updater..."
echo "This is made to be run by a compatability plugin."

git pull
sudo systemctl restart openloop

echo "Completed, checking status"

sudo systemctl status openloop
