/* in mysite/__init__.py */
use midterm_django;

--
-- Create model Like
--
CREATE TABLE `blog_like` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY
    );
--
-- Create model User
--
CREATE TABLE `blog_user` (
    `name` varchar(20) NOT NULL PRIMARY KEY, 
    `password` varchar(20) NOT NULL, 
    `email` varchar(254) NOT NULL
    );
--
-- Create model Post
--
CREATE TABLE `blog_post` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `content` varchar(200) NOT NULL, 
    `time` datetime(6) NOT NULL, 
    `author_id` varchar(20) NOT NULL
    );
--
-- Create model Notify
--
CREATE TABLE `blog_notify` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `read` bool NOT NULL, 
    `like_id` integer NOT NULL, 
    `user_id` varchar(20) NOT NULL);
--
-- Add field post_id to like
--
ALTER TABLE `blog_like` 
    ADD COLUMN `post_id_id` integer NOT NULL , 
    ADD CONSTRAINT `blog_like_post_id_id_008d12a2_fk_blog_post_id` 
        FOREIGN KEY (`post_id_id`) REFERENCES `blog_post`(`id`) ON DELETE CASCADE;
--
-- Add field username to like
--
ALTER TABLE `blog_like` 
    ADD COLUMN `username_id` varchar(20) NOT NULL , 
    ADD CONSTRAINT `blog_like_username_id_afe82c7c_fk_blog_user_name` 
        FOREIGN KEY (`username_id`) REFERENCES `blog_user`(`name`) ON DELETE CASCADE;
--
-- Create model Follow
--
CREATE TABLE `blog_follow` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `be_followed_id` varchar(20) NOT NULL, 
    `following_id` varchar(20) NOT NULL);

ALTER TABLE `blog_post` 
    ADD CONSTRAINT `blog_post_author_id_dd7a8485_fk_blog_user_name` 
        FOREIGN KEY (`author_id`) REFERENCES `blog_user` (`name`) ON DELETE CASCADE;

ALTER TABLE `blog_notify` 
    ADD CONSTRAINT `blog_notify_like_id_3f3259e2_fk_blog_like_id` 
        FOREIGN KEY (`like_id`) REFERENCES `blog_like` (`id`) ON DELETE CASCADE;

ALTER TABLE `blog_notify` 
    ADD CONSTRAINT `blog_notify_user_id_cfebabaf_fk_blog_user_name` 
        FOREIGN KEY (`user_id`) REFERENCES `blog_user` (`name`) ON DELETE CASCADE;

ALTER TABLE `blog_follow` 
    ADD CONSTRAINT `blog_follow_be_followed_id_b50ef869_fk_blog_user_name` 
        FOREIGN KEY (`be_followed_id`) REFERENCES `blog_user` (`name`) ON DELETE CASCADE;

ALTER TABLE `blog_follow` 
    ADD CONSTRAINT `blog_follow_following_id_d939b09d_fk_blog_user_name` 
        FOREIGN KEY (`following_id`) REFERENCES `blog_user` (`name`) ON DELETE CASCADE;
