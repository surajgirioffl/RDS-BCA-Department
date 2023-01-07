/*
 * MySQL
 * Schema for database `StudyMaterials` or `rdsbca$Sem1StudyMaterials', `rdsbca$Sem2StudyMaterials' and so on.
 * Created by: Suraj Kumar Giri
 * Created on: 7th Jan 2023
 */
----
-- 1. Table `Ignou`
----
CREATE TABLE `Ignou` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL,
    `SubjectCode` SMALLINT UNSIGNED NOT NULL,
    `DisplayOrder` DECIMAL(5, 2) NOT NULL DEFAULT 0,
);

----
-- 2. Table `Ebooks`
----
CREATE TABLE `Ebooks` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL,
    `SubjectCode` SMALLINT UNSIGNED NOT NULL,
    `DisplayOrder` DECIMAL(5, 2) NOT NULL DEFAULT 0,
);

----
-- 3. Table `Others`
----
CREATE TABLE `Others` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL,
    `SubjectCode` SMALLINT UNSIGNED NOT NULL,
    `DisplayOrder` DECIMAL(5, 2) NOT NULL DEFAULT 0,
);

----
-- 4. Table `Externals`
----
CREATE TABLE `Externals` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `Link` CHAR(255) PRIMARY KEY NOT NULL,
    `SubjectCode` SMALLINT UNSIGNED NOT NULL,
    `DisplayOrder` DECIMAL(5, 2) NOT NULL DEFAULT 0,
);