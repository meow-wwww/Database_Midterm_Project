in mysite/__init__.py
--
-- Create model Post
--
CREATE TABLE `blog_post` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `content` varchar(200) NOT NULL, 
    `time` datetime(6) NOT NULL);
--
-- Create model User
--
CREATE TABLE `blog_user` (
    `name` varchar(20) NOT NULL PRIMARY KEY, 
    `password` varchar(20) NOT NULL, 
    `email` varchar(254) NOT NULL);
--
-- Create model Reply
--
CREATE TABLE `blog_reply` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `content` varchar(100) NOT NULL, 
    `post_id_id` integer NOT NULL, 
    `receiver_id_id` varchar(20) NOT NULL, 
    `sender_id_id` varchar(20) NOT NULL);
--
-- Create model Like
--
CREATE TABLE `blog_like` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `post_id_id` integer NOT NULL, `username_id` varchar(20) NOT NULL);
--
-- Create model Follow
--
CREATE TABLE `blog_follow` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `be_followed_id` varchar(20) NOT NULL, 
    `following_id` varchar(20) NOT NULL);
    
ALTER TABLE `blog_reply` ADD CONSTRAINT `blog_reply_post_id_id_71220e59_fk_blog_post_id` FOREIGN KEY (`post_id_id`) REFERENCES `blog_post` (`id`);
ALTER TABLE `blog_reply` ADD CONSTRAINT `blog_reply_receiver_id_id_c887c477_fk_blog_user_name` FOREIGN KEY (`receiver_id_id`) REFERENCES `blog_user` (`name`);
ALTER TABLE `blog_reply` ADD CONSTRAINT `blog_reply_sender_id_id_d5ac6784_fk_blog_user_name` FOREIGN KEY (`sender_id_id`) REFERENCES `blog_user` (`name`);
ALTER TABLE `blog_like` ADD CONSTRAINT `blog_like_post_id_id_008d12a2_fk_blog_post_id` FOREIGN KEY (`post_id_id`) REFERENCES `blog_post` (`id`);
ALTER TABLE `blog_like` ADD CONSTRAINT `blog_like_username_id_afe82c7c_fk_blog_user_name` FOREIGN KEY (`username_id`) REFERENCES `blog_user` (`name`);
ALTER TABLE `blog_follow` ADD CONSTRAINT `blog_follow_be_followed_id_b50ef869_fk_blog_user_name` FOREIGN KEY (`be_followed_id`) REFERENCES `blog_user` (`name`);
ALTER TABLE `blog_follow` ADD CONSTRAINT `blog_follow_following_id_d939b09d_fk_blog_user_name` FOREIGN KEY (`following_id`) REFERENCES `blog_user` (`name`);
