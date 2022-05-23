-- 帖子id和点赞数（0赞也包括）
use midterm_django;
create view post_id_likenum(id, likenum)
as (
        select blog_post.id id, 0 likenum
        from blog_post
        where blog_post.id not in (select post_id_id from blog_like)
    union
        select blog_like.post_id_id id, count(*) likenum
        from blog_like
        group by blog_like.post_id_id
);


-- xx关注的人的帖子（id, author, content, time, likenum）
-- 没用上，后面有完善版
use midterm_django;
create view my_follow_post(id, author, content, time, likenum, myid)
as(
    select blog_post.id, blog_post.author_id, blog_post.content, blog_post.time, likenum, blog_follow.following_id
    from post_id_likenum, blog_post, blog_follow
    where blog_follow.be_followed_id = blog_post.author_id
        and post_id_likenum.id = blog_post.id
);
    -- 测试代码
    /* use midterm_django;
    select id, author, content, time, likenum
    from my_follow_post
    where my_follow_post.myid = 'wxy'; */


-- 某人发布的帖子(id, author, content, time, likenum)
-- 没用上，后面有完善版
use midterm_django;
create view ones_post(id, author, content, time, likenum, myid)
as(
    select blog_post.id, blog_post.author_id, blog_post.content, blog_post.time, likenum, blog_post.author_id
    from post_id_likenum, blog_post
    where post_id_likenum.id = blog_post.id
);
    -- 测试代码
    /* use midterm_django;
    select id, author, content, time, likenum
    from ones_post
    where ones_post.myid = 'wxy'; */


use midterm_django;
create view someone_like_or_not (id, like_or_not, myid)
as (
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
    )
);
    -- 测试代码
    /* use midterm_django;
    select id, like_or_not
    from someone_like_or_not
    where someone_like_or_not.myid = 'wxy' */


-- xx关注的人的帖子,以及是否点赞(id, author, content, time, likenum, myid, like_or_not)
use midterm_django;
create view my_follow_post_bool(id, author, content, time, likenum, myid, like_or_not)
as(
    select my_follow_post.id, my_follow_post.author, my_follow_post.content, my_follow_post.time, my_follow_post.likenum, my_follow_post.myid, someone_like_or_not.like_or_not
    from my_follow_post, someone_like_or_not
    where someone_like_or_not.myid = my_follow_post.myid
        and someone_like_or_not.id = my_follow_post.id
);
    -- 测试代码
    /* use midterm_django;
    select id, author, content, time, likenum, like_or_not from my_follow_post_bool
    where my_follow_post_bool.myid = 'wxy'; */


-- 某人发布的帖子,以及是否点赞(id, author, content, time, likenum, hisid, myid, like_or_not)
use midterm_django;
create view ones_post_bool(id, author, content, time, likenum, hisid, myid, like_or_not) 
    -- myid:查看的是<谁>; like_or_not: <我>点赞没有
    -- 两个变量,分别对应hisid和myid
as (
    select ones_post.id, ones_post.author, ones_post.content, ones_post.time, ones_post.likenum, ones_post.myid, blog_user.name, someone_like_or_not.like_or_not
    from ones_post, someone_like_or_not, blog_user
    where someone_like_or_not.myid = blog_user.name
        and someone_like_or_not.id = ones_post.id
);
    -- 测试代码
    /* use midterm_django;
    select id, author, content, time, likenum, like_or_not
    from ones_post_bool
    where ones_post_bool.myid = 'wxy' and ones_post_bool.hisid='xxz'; */


-- 显示所有视图
/* use midterm_django;
show table status where comment='trigger'; */



-- 触发器
use midterm_django;
create trigger like_notification after insert on blog_like for each row
insert into blog_notify values (DEFAULT, false, NEW.id, NEW.username_id);

/* use midterm_django;
drop trigger like_notification; */