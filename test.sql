use midterm_django;

select follow_post.id, follow_post.author, follow_post.content, follow_post.time, count(*) likenum 
from (
    select blog_post.id, blog_post.content, blog_post.author_id, blog_post.time 
    from blog_post, blog_follow
    where blog_post.author_id = blog_follow.be_followed_id and blog_follow.following_id = 'wxy'
    ) as follow_post(id, content, author, time), blog_like
where follow_post.id = blog_like.post_id_id
group by follow_post.id;

insert into blog_post value(DEFAULT, 'hello', DEFAULT, 'wxy');

select * from blog_user where blog_user.name like '%xz%';