/*
 * MySQL
 * Schema for database `study_materials` or `rdsbca$sem1_study_materials', `rdsbca$sem2_study_materials' and so on.
 * Created by: Suraj Kumar Giri
 * Created on: 7th Jan 2023
 * Last updated on: 10th Jan 2023
 */
----
-- 1. Table `ignou`
----
CREATE TABLE IF NOT EXISTS `ignou` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL,
    `SubjectCode` SMALLINT UNSIGNED NOT NULL,
    `DisplayOrder` DECIMAL(5, 2) NOT NULL DEFAULT 0
);

----
-- 2. Table `ebooks`
----
CREATE TABLE IF NOT EXISTS `ebooks` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL,
    `SubjectCode` SMALLINT UNSIGNED NOT NULL,
    `DisplayOrder` DECIMAL(5, 2) NOT NULL DEFAULT 0
);

----
-- 3. Table `others`
----
CREATE TABLE IF NOT EXISTS `others` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `FileId` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL,
    `SubjectCode` SMALLINT UNSIGNED NOT NULL,
    `DisplayOrder` DECIMAL(5, 2) NOT NULL DEFAULT 0
);

----
-- 4. Table `externals`
----
CREATE TABLE IF NOT EXISTS `externals` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `Link` VARCHAR(200) PRIMARY KEY NOT NULL,
    `SubjectCode` SMALLINT UNSIGNED NOT NULL,
    `DisplayOrder` DECIMAL(5, 2) NOT NULL DEFAULT 0
);