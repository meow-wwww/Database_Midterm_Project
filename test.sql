-- 我关注的人的帖子
use midterm_django;
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