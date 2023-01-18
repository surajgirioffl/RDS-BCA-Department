-- MySQL
-- Schema for database `dynamic_contents` or `rdsbca$dynamic_contents`
-- Created by: Suraj Kumar Giri
-- Created on: 16th Jan 2023
-- Last updated on: 18th Jan 2023
----
-- 1. Table `notice`
----
CREATE TABLE IF NOT EXISTS `notice` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `TopMarquee` VARCHAR(300) NOT NULL,
    `TopMarqueeLink` VARCHAR(100) NOT NULL,
    `Title` VARCHAR(300) NOT NULL,
    `DocsDownloadTitle` VARCHAR(200) NOT NULL,
    `DocsDownloadLink` VARCHAR(100) DEFAULT NULL,
    `ButtonTitle` VARCHAR(200) DEFAULT NULL,
    `ButtonLink` VARCHAR(100) DEFAULT NULL,
    `BlinkerTitle` VARCHAR(80) NOT NULL,
    `BlinkingText` VARCHAR(50) NOT NULL,
    `BottomMarquee1` VARCHAR(300) NOT NULL,
    `BottomMarquee2` VARCHAR(300) DEFAULT NULL,
    `BottomMarquee3` VARCHAR(300) DEFAULT NULL,
    `DateModified` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
);

----
-- 2. Table `credits`
----
CREATE TABLE IF NOT EXISTS `credits`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `Name` VARCHAR(50) NOT NULL,
    `Designation` VARCHAR(50) NOT NULL,
    `Contributions` VARCHAR(200) NOT NULL,
    `ContactTitle` VARCHAR(50) DEFAULT NULL,
    `ContactLink` VARCHAR(100) DEFAULT NULL,
);

----
-- 3. Table `sources`
----
CREATE TABLE IF NOT EXISTS `sources`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `Name` VARCHAR(50) NOT NULL,
    `Contributions` VARCHAR(200) NOT NULL,
    `Link` VARCHAR(100) DEFAULT NULL,
);