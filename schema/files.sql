-- MySQL
-- Schema for database `Files` or `rdsbca$Files`
-- Created by: Suraj Kumar Giri
-- Created on: 7th Jan 2023
-- Last updated on: 10th Jan 2023
----
-- 1. Table `Files`
----
CREATE TABLE IF NOT EXISTS Files(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL,
    `Title` VARCHAR(255) NOT NULL,
    `DateModified` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `DownloadCount` MEDIUMINT UNSIGNED NOT NULL DEFAULT 0
);

----
-- First execute above query then run below query because of foreign key constraint.
-- 2. Table `FilesPath`
----
CREATE TABLE IF NOT EXISTS FilesPath(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL,
    `FilePath` VARCHAR(400) NOT NULL UNIQUE,
    FOREIGN KEY (FileId) REFERENCES Files(FileId)
);

----
-- 3. Table `Drive`
----
CREATE TABLE IF NOT EXISTS Drive(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL,
    `ViewLink` VARCHAR(200) NOT NULL UNIQUE,
    `DownloadLink` VARCHAR(200) NOT NULL UNIQUE,
    FOREIGN KEY (FileId) REFERENCES Files(FileId)
);

----
-- 4. Table `FileContentsInfo`
----
CREATE TABLE IF NOT EXISTS FileContentsInfo(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL,
    `Description` VARCHAR(800) NOT NULL,
    `Keywords` VARCHAR(600) NOT NULL,
    FOREIGN KEY (FileId) REFERENCES Files(FileId)
);