use midterm_django;
select * from who_likes_me where who_likes_me.author_id = 'wxy' and who_likes_me.read = 0;

use midterm_django;
select * from who_likes_me;

use midterm_django;
select blog_post.author_id, blog_post.content, blog_like.username_id, blog_notify.read
    from blog_notify, blog_like, blog_post
    where blog_notify.like_id = blog_like.id
        and blog_like.post_id_id = blog_post.id