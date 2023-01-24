-- MySQL
-- Schema for database `files` or `rdsbca$files`
-- Created by: Suraj Kumar Giri
-- Created on: 7th Jan 2023
-- Last updated on: 24th Jan 2023
----
-- 1. Table `files`
----
CREATE TABLE IF NOT EXISTS files(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `Title` VARCHAR(255) NOT NULL,
    `Access` ENUM('Public', 'Private', 'Restricted') NOT NULL DEFAULT 'Public',
    `ServeVia` ENUM('FileSystem', 'Drive') NOT NULL DEFAULT 'Drive'
);

----
-- First execute above query then run below query because of foreign key constraint.
-- 2. Table `files_path`
----
CREATE TABLE IF NOT EXISTS files_path(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `FilePath` VARCHAR(400) NOT NULL UNIQUE,
    FOREIGN KEY (FileId) REFERENCES Files(FileId)
);

----
-- 3. Table `drive`
----
CREATE TABLE IF NOT EXISTS drive(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `ViewLink` VARCHAR(200) NOT NULL UNIQUE,
    `DownloadLink` VARCHAR(200) NOT NULL UNIQUE,
    FOREIGN KEY (FileId) REFERENCES Files(FileId)
);

----
-- 4. Table `file_contents_info`
----
CREATE TABLE IF NOT EXISTS file_contents_info(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `Description` VARCHAR(600) NOT NULL,
    `Keywords` VARCHAR(500) NOT NULL,
    FOREIGN KEY (FileId) REFERENCES Files(FileId)
);

----
-- 5. Table `files_metadata`
----
CREATE TABLE IF NOT EXISTS `files_metadata`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `FileName` VARCHAR(100) NOT NULL,
    `DownloadName` VARCHAR(100) NOT NULL,
    `Extension` VARCHAR(10) NOT NULL,
    `Size` VARCHAR(20) NOT NULL,
    INDEX `ExtensionIndex` (Extension),
    FOREIGN KEY (FileId) REFERENCES Files(FileId)
);

----
-- 6. Table `files_type`
----
CREATE TABLE IF NOT EXISTS `files_type`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `Extension` VARCHAR(10) NOT NULL PRIMARY KEY,
    `FileType` VARCHAR(30) NOT NULL,
    FOREIGN KEY (Extension) REFERENCES files_metadata(Extension)
);

----
-- 7. Table `files_info`
----
CREATE TABLE IF NOT EXISTS `files_info`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `Category` VARCHAR(50) NOT NULL,
    `FileFor` VARCHAR(50) NOT NULL,
    `DateCreated` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `DateModified` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `Tags` VARCHAR(200) NOT NULL,
    FOREIGN KEY (FileId) REFERENCES Files(FileId)
);

----
-- 8. Table `files_Tracking`
----
CREATE TABLE IF NOT EXISTS `files_tracking`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `AccessCount` MEDIUMINT UNSIGNED NOT NULL DEFAULT 0,
    `DownloadCount` MEDIUMINT UNSIGNED NOT NULL DEFAULT 0,
    `LastAccessed` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `LastDownloaded` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (FileId) REFERENCES Files(FileId)
);

----
-- 9. Table `creditors_info`
----
CREATE TABLE IF NOT EXISTS `creditors_info` (
    `Id` SMALLINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `Name` VARCHAR(100) NOT NULL,
    `Username` VARCHAR(50) UNIQUE DEFAULT NULL,
    `Designation` VARCHAR(50) DEFAULT NULL,
    `Contact` VARCHAR(100) UNIQUE DEFAULT NULL,
);

----
-- 10. Table `credits`
-- Write username instead of full name in attributes such as UploadedBy, LastModifiedBy, ApprovedBy etc to identify the user from users and related database.
----
CREATE TABLE IF NOT EXISTS `credits`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `Submittedby` VARCHAR(50) DEFAULT NULL,
    `SubmittedOn` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `UploadedBy` VARCHAR(50) NOT NULL,
    `UploadedOn` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `LastModifiedBy` VARCHAR(50) NOT NULL,
    `LastModifiedOn` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ApprovedBy` VARCHAR(50) NOT NULL,
    `ApprovedOn` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `RootSource` VARCHAR(100) NOT NULL,
    INDEX `RootSourceIndex` (RootSource),
    FOREIGN KEY (FileId) REFERENCES Files(FileId)
);

----
-- 11. Table `root_sources`
----
CREATE TABLE IF NOT EXISTS `root_sources` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `RootSource` VARCHAR(100) NOT NULL PRIMARY KEY,
    `SourceFileLink` VARCHAR(200) DEFAULT NULL,
    `ContactSource` VARCHAR(100) NOT NULL,
    FOREIGN KEY (RootSource) REFERENCES credits(RootSource)
);