create table if not exists video(

    id varchar(50) primary key, 
    title varchar(100)

);


create table if not exists playlist(

    id varchar(50) primary key,
    name varchar(100)
);


create table if not exists playlist_video(


    playlist_id varchar(50),
    video_id varchar(50),
    last_seen datetime,
    gone_missing datetime,

    primary key(playlist_id, video_id),
    foreign key(playlist_id) references playlist(id),
    foreign key(video_id) references video(id)

);



