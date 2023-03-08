/*
 * MySQL
 * Schema for database `access_control` or `rdsbca$access_control`.
 * Created by: Suraj Kumar Giri
 * Created on: 6th March 2023
 * Last updated 8th March 2023
 */
----
-- 1. Table `moderator_administrator`
-- Username of moderator/adminstrator will be differ from that of normal user even that moderator/adminstrator is one of the normal user.
-- Username will be equal to "<moderator/admin>+FirstName+Id" where for moderator, Id = ModeratorId and for adminstrator, Id = AdminId.
----
CREATE TABLE IF NOT EXISTS `moderator_administrator` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `Id` INT UNSIGNED PRIMARY KEY NOT NULL,
    `Email` VARCHAR(100) NOT NULL UNIQUE,
    `Username` VARCHAR(50) UNIQUE NOT NULL,
    `Role` ENUM('admin', 'moderator') NOT NULL,
);