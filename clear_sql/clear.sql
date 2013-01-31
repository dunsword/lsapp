BEGIN;
DROP TABLE `album_document`;
DROP TABLE `album_album`;
DROP TABLE `album_taobaoitem`;
DROP TABLE `base_userprofile`;
ALTER TABLE `auth_user_user_permissions` DROP FOREIGN KEY `user_id_refs_id_4dc23c39`;
ALTER TABLE `auth_user_groups` DROP FOREIGN KEY `user_id_refs_id_40c41112`;
DROP TABLE `auth_user`;
DROP TABLE `auth_user_user_permissions`;
DROP TABLE `auth_user_groups`;
ALTER TABLE `auth_group_permissions` DROP FOREIGN KEY `group_id_refs_id_f4b32aac`;
DROP TABLE `auth_group`;
DROP TABLE `auth_group_permissions`;
DROP TABLE `auth_permission`;
DROP TABLE `django_content_type`;
DROP TABLE `django_session`;
DROP TABLE `django_site`;

COMMIT;
