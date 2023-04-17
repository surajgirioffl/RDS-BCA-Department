-- MySQL
-- Schema for database `files` or `rdsbca$files`
-- Created by: Suraj Kumar Giri
-- Created on: 7th Jan 2023
-- Last updated on: 18th April 2023
----
-- 1. Table `files`
-- FileId should be an unique 8 digit number. It will be used to identify file. It will be used to access file.
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
-- Write Description in sentence case (In such way that it will describe file effectively and it will presented to user as file description)
-- Write Keywords in small case comma separated words (space allowed in a keyword). Space is compulsory after comma but strictly not allowed before comma.
-- Keep in mind, Keywords are related to file contents. It will be used to search specific content. It should be content oriented.
-- E.g: "python, numpy, data science, machine learning, artificial intelligence, deep learning etc."
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
-- File name will same as file name in file system or drive.
-- Download name should be in Proper Case (First letter of each word must be in capital letter). It is also called as Title Case.
-- File Size must be in MB (Megabytes) (decimal value allowed)
----
CREATE TABLE IF NOT EXISTS `files_metadata`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `FileName` VARCHAR(100) NOT NULL,
    `DownloadName` VARCHAR(100) NOT NULL,
    `Extension` VARCHAR(10) NOT NULL,
    `Size` DOUBLE UNSIGNED NOT NULL,
    INDEX `ExtensionIndex` (Extension),
    FOREIGN KEY (FileId) REFERENCES Files(FileId)
);

----
-- 6. Table `files_type`
-- Extension specifies the type of file such as pdf, doc, docx, ppt, pptx, xls, xlsx, txt, etc.
-- FileType specifies the type of file such as image, document, video, audio, etc. 
-- Use small case for Extension and FileType.
----
CREATE TABLE IF NOT EXISTS `files_type`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `Extension` VARCHAR(10) NOT NULL PRIMARY KEY,
    `FileType` VARCHAR(30) NOT NULL,
    FOREIGN KEY (Extension) REFERENCES files_metadata(Extension)
);

----
-- 7. Table `files_info`
-- Category specifies the type of file such as notes, question paper, assignment, project, previous year question paper, etc.
-- FileFor specifies the reason for uploading this file such as for study purpose, for reference, for practice, etc.
-- Tags are used to search file. It is also used to categorize file. It is also used to find related files. 
-- In this Schema, Tags are different from Keywords. Keywords contains content related words and Tags contains file related words.
-- So, Tags must specify the file. It should be file oriented.
-- E.g: "python handbook, python notes, python tutorial, etc."
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
-- It may possible that submitter is not a registered user. So, it will have only Id, Name, Contact and Designation(not always).
-- AccountId is the id of a registered user/teacher which is from database such as rdsbca$users/rdsbca$bca.teachers.
----
CREATE TABLE IF NOT EXISTS `creditors_info` (
    `Id` SMALLINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `Name` VARCHAR(100) NOT NULL,
    `Email` VARCHAR(100) UNIQUE NOT NULL,
    `Designation` VARCHAR(50) DEFAULT NULL,
    `Username` VARCHAR(50) UNIQUE DEFAULT NULL,
    `AccountId` INT UNSIGNED UNIQUE DEFAULT NULL,
    `Contact` VARCHAR(100) UNIQUE DEFAULT NULL
);

----
-- 10. Table `root_sources`
----
CREATE TABLE IF NOT EXISTS `root_sources` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `Id` INT UNSIGNED PRIMARY KEY NOT NULL,
    `Name` VARCHAR(100) NOT NULL UNIQUE,
    `ContactLink` VARCHAR(100) NOT NULL
);

----
-- 11. Table `credits`
-- Write Id of table 'creditors_info' instead of full name or username in attributes such as UploadedBy, LastModifiedBy, ApprovedBy etc to identify the user from users and related databases.
----
CREATE TABLE IF NOT EXISTS `credits`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `SubmitterId` SMALLINT UNSIGNED NOT NULL,
    `SubmittedOn` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `UploaderId` SMALLINT UNSIGNED NOT NULL,
    `UploadedOn` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ModifierId` SMALLINT UNSIGNED NOT NULL,
    `LastModifiedOn` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ApproverId` SMALLINT UNSIGNED NOT NULL,
    `ApprovedOn` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `RootSourceFileLink` VARCHAR(200) DEFAULT NULL,
    `RootSourceId` INT UNSIGNED NOT NULL,
    INDEX `RootSourceIndex` (RootSourceId),
    FOREIGN KEY (FileId) REFERENCES Files(FileId),
    FOREIGN KEY (SubmitterId) REFERENCES creditors_info(Id),
    FOREIGN KEY (UploaderId) REFERENCES creditors_info(Id),
    FOREIGN KEY (ModifierId) REFERENCES creditors_info(Id),
    FOREIGN KEY (ApproverId) REFERENCES creditors_info(Id),
    FOREIGN KEY (RootSourceId) REFERENCES root_sources(Id)
);