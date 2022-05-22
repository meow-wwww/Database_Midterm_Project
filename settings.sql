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