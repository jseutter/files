# SQL Server

## SQL Server docker container
docker pull mcr.microsoft.com/mssql/server
docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=password' -p 1433:1433 -d mcr.microsoft.com/mssql/server:2017-latest

Checking that the server is reachable:
curl http://server_hostname:1433

This should exit with "Empty reply from server"

## RHEL 7 driver install
- Red Hat Enterprise Server 7 and Oracle Linux 7
curl https://packages.microsoft.com/config/rhel/7/prod.repo > /etc/yum.repos.d/mssql-release.repo

ACCEPT_EULA=Y yum install -y msodbcsql17
ACCEPT_EULA=Y yum install -y mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
yum install -y unixODBC-devel

source: https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15#microsoft-odbc-driver-13-for-sql-server

## Logging in as admin locally
./sqlcmd -S localhost -U SA -P "Password1"

 - SA is the sysadmin login
 - sqlcmd is normally on the path, but if it isn't, it is in /opt/mssql-tools/bin

## Listing databases on a server
select name, database_id, create_date from sys.databases
go

## Creating a new "login"
create login foo with password = 'Foobarbaz1'
go

## Giving the login access to resources (user)

## Connecting from Python with pyodbc
import pyodbc
c = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:192.168.1.125;DATABASE=tempdb;UID=foo;PWD=Foobarbaz1')
c.execute('select 1').fetchall()

