git add .
git commit -m "deploying existing"
git push
ssh root@137.184.117.22 'sudo -u user /home/user/deploy_bazarcasa.ma.sh'
