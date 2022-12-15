create table download_user (
    user_id varchar(8) not null primary key
    , password varchar(64) not null
    , role_code character(1) not null
);
