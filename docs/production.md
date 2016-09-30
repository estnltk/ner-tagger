# Production Environment
This document demonstrates example environment setup for CentOS 7.7.5.

### Postgres 9.5
Install postgres 9.5, create user *distorti* and database *nertagger*:

    su -
    yum localinstall https://download.postgresql.org/pub/repos/yum/9.5/redhat/rhel-7-x86_64/pgdg-centos95-9.5-2.noarch.rpm
    yum list postgres95*
    yum install postgres95-server libpqxx-devel.x86_64
    
    su postgres
    export PGDATA=/var/lib/pgsql/9.5/data
    /usr/pgsql-9.5/bin/initdb
    createrole -d distorti
    su -
    sudo chkconfig postgresql-9.5 on

    su distorti
    createdb nertagger
    psql -d nertagger

More details: https://wiki.postgresql.org/wiki/YUM_Installation


### Apache Web Server
    yum install httpd mod_wsgi
    service httpd start

### Firewall
Open port 80 for Apache:

    yum install iptables-services
    iptables -I INPUT -p tcp --dport 80 -m state --state NEW -j ACCEPT
    service iptables save

### Django debug toolbar for ajax requests:

https://pypi.python.org/pypi/django-debug-panel/0.8.2