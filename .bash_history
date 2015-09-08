ls
ssh-keygen 
more /opt/smartforceplus/.ssh/id_rsa.pub
git remote add origin git@github.com:smatforce/SmartForceplus.git
git push origin master
git pull origin master
ls
git push origin master
git remote add origin git@github.com:smatforce/SmartForceplus.git
git push origin master
git remote add origin smartforce@github.com:smatforce/SmartForceplus.git
git push origin master
git push -f
git push origin master
ls
ls -al -h
cd /etc
cat crontab 
more /var/script.sh 
vi /var/script.sh 
su - postgres -c "pg_dump smartforceplus > /opt/smartforceplus/smartforceplus-sql-$din"
exit
