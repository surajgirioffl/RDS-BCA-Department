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
-- Username must be unique among moderator_administrator table in this database and users table in users database. (Because in blocklist table, username is used and constraints are UNIQUE, NOT NULL etc and tuple may be from moderators/administrators/normal users table).
----
CREATE TABLE IF NOT EXISTS `moderator_administrator` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `Id` INT UNSIGNED PRIMARY KEY NOT NULL,
    `Email` VARCHAR(100) NOT NULL UNIQUE,
    `Username` VARCHAR(50) UNIQUE NOT NULL,
    `Role` ENUM('admin', 'moderator') NOT NULL,
);

----
-- 2. Table `moderators`
----
CREATE TABLE IF NOT EXISTS `moderators` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `ModeratorId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `FirstName` VARCHAR(50) NOT NULL,
    `LastName` VARCHAR(50) NOT NULL,
    FOREIGN KEY (`ModeratorId`) REFERENCES moderator_administrator(`Id`) ON DELETE CASCADE
);

----
-- 3. Table `administrators`
----
CREATE TABLE IF NOT EXISTS `administrators` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `AdminId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `FirstName` VARCHAR(50) NOT NULL,
    `LastName` VARCHAR(50) NOT NULL,
    FOREIGN KEY (`AdminId`) REFERENCES moderator_administrator(`Id`) ON DELETE CASCADE
);

----
-- 4. Table `access_statistics`
-- This statics is independent from normal user statistics. It will be updated only if moderator/adminstrator visit the moderator/adminstrator dashboard.
----
CREATE TABLE IF NOT EXISTS `access_statistics`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `Id` INT UNSIGNED PRIMARY KEY NOT NULL,
    `LastVisited` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `VisitCount` INT UNSIGNED DEFAULT 0,
    `RegisteredOn` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`Id`) REFERENCES moderator_administrator(`Id`)
);