-- “我”关注的人的帖子
use midterm_django;
select blog_post.id, blog_post.author_id, blog_post.content, blog_post.time, likenum
from post_id_likenum, blog_post, blog_follow
where blog_follow.following_id = 'wxy'
    and blog_follow.be_followed_id = blog_post.author_id
    and post_id_likenum.id = blog_post.id;

-- 再加一个“我”赞没赞
use midterm_django;

select blog_post.id id, 1 likebyme
from blog_post
where blog_post.id in (
    select blog_like.post_id_id from blog_like
    where blog_like.username_id = 'xxz'
)
union
select blog_post.id id, 0 likebyme
from blog_post
where blog_post.id not in (
    select blog_like.post_id_id from blog_like
    where blog_like.username_id = 'xxz'
);

-- 再加一个“我”赞没赞 -- view
use midterm_django;
select post_t.id, 1 like_by_me, user_t.name myid
from blog_post post_t, blog_user user_t
where exists (
    select * from blog_like
    where blog_like.post_id_id = post_t.id
        and blog_like.username_id = user_t.name
)
union
select post_t.id, 0 like_by_me, user_t.name myid
from blog_post post_t, blog_user user_t
where not exists (
    select * from blog_like
    where blog_like.post_id_id = post_t.id
        and blog_like.username_id = user_t.name
);



use midterm_django;
select ones_post.id, ones_post.author, ones_post.content, ones_post.time, ones_post.likenum, ones_post.myid, someone_like_or_not.like_or_not
    from ones_post, someone_like_or_not
    where someone_like_or_not.myid = ones_post.myid
        and someone_like_or_not.id = ones_post.id;



select blog_post.id id, 1 likebyme, like_table.username_id myid
from blog_post, blog_like like_table
where blog_post.id, like_table.username_id in(
    select blog_like.post_id_id, blog_like.username_id from blog_like
    /* where blog_like.username_id = 'xxz' */
)
union
select blog_post.id id, 0 likebyme, like_table.username_id myid
from blog_post, blog_like like_table
where blog_post.id, like_table.username_id not in (
    select blog_like.post_id_id, blog_like.username_id from blog_like
    /* where blog_like.username_id = 'xxz' */
);


select blog_post.id, blog_post.author_id, blog_post.content, blog_post.time, likenum
from post_id_likenum, blog_post, blog_follow
where blog_follow.following_id = 'wxy'
    and blog_follow.be_followed_id = blog_post.author_id
    and post_id_likenum.id = blog_post.id;


-- 某人的帖子
use midterm_django;
select blog_post.id, blog_post.author_id, blog_post.content, blog_post.time, likenum
from post_id_likenum, blog_post
where blog_post.author_id = 'wxy'
    and post_id_likenum.id = blog_post.id;


select follow_post.id, follow_post.author, follow_post.content, follow_post.time, count(*) likenum 
from (
    select blog_post.id, blog_post.content, blog_post.author_id, blog_post.time 
    from blog_post, blog_follow
    where blog_post.author_id = blog_follow.be_followed_id and blog_follow.following_id = 'wxy'
    ) as follow_post(id, content, author, time), blog_like
where follow_post.id = blog_like.post_id_id
group by follow_post.id
union
select follow_post.id, follow_post.author, follow_post.content, follow_post.time, 0 likenum 
from (
    select blog_post.id, blog_post.content, blog_post.author_id, blog_post.time 
    from blog_post, blog_follow
    where blog_post.author_id = blog_follow.be_followed_id and blog_follow.following_id = 'wxy'
    ) as follow_post(id, content, author, time)
where follow_post.id not in (select post_id_id from blog_like);






use midterm_django;
select blog_post.id, blog_post.content, blog_post.author_id, blog_post.time 
    from blog_post, blog_follow
    where blog_post.author_id = blog_follow.be_followed_id and blog_follow.following_id = 'wxy';


select follow_post.id, follow_post.author, follow_post.content, follow_post.time, count(*) likenum 
from (
    select blog_post.id, blog_post.content, blog_post.author_id, blog_post.time 
    from blog_post, blog_follow 
    where blog_post.author_id = blog_follow.be_followed_id and blog_follow.following_id = 'wxy'
    ) as follow_post(id, content, author, time), blog_like 
where follow_post.id = blog_like.post_id_id 
group by follow_post.id


insert into blog_post value(DEFAULT, 'hello', DEFAULT, 'wxy');

select * from blog_user where blog_user.name like '%xz%';


use midterm_django;
select id, author, content, time, likenum
from my_follow_post
where my_follow_post.myid = 'wxy';