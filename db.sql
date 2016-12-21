create database pythoney;
create user 'pythoney'@'localhost' identified by 'pythoney';
grant all on pythoney.* to 'pythoney'@'localhost';
use pythoney;
create table connections(id int auto_increment, time timestamp, server_port int, source_address varchar(16), source_country varchar(8), source_port int, data varchar(1024), primary key (id));
