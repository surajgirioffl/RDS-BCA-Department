-- MySQL
-- Schema for database `files` or `rdsbca$files`
-- Created by: Suraj Kumar Giri
-- Created on: 7th Jan 2023
-- Last updated on: 10th Jan 2023
----
-- 1. Table `files`
----
CREATE TABLE IF NOT EXISTS files(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL,
    `Title` VARCHAR(255) NOT NULL,
    `DateCreated` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `DateModified` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `DownloadCount` MEDIUMINT UNSIGNED NOT NULL DEFAULT 0
);

----
-- First execute above query then run below query because of foreign key constraint.
-- 2. Table `files_path`
----
CREATE TABLE IF NOT EXISTS files_path(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL,
    `FilePath` VARCHAR(400) NOT NULL UNIQUE,
    FOREIGN KEY (FileId) REFERENCES Files(FileId)
);

----
-- 3. Table `drive`
----
CREATE TABLE IF NOT EXISTS drive(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL,
    `ViewLink` VARCHAR(200) NOT NULL UNIQUE,
    `DownloadLink` VARCHAR(200) NOT NULL UNIQUE,
    FOREIGN KEY (FileId) REFERENCES Files(FileId)
);

----
-- 4. Table `file_contents_info`
----
CREATE TABLE IF NOT EXISTS file_contents_info(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL,
    `Description` VARCHAR(800) NOT NULL,
    `Keywords` VARCHAR(600) NOT NULL,
    FOREIGN KEY (FileId) REFERENCES Files(FileId)
);