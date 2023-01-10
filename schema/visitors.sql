/*
 * MySQL
 * Schema for database `visitors` or `rdsbca$visitors`
 * Created by: Suraj Kumar Giri
 * Created on: 10th Jan 2023
 * Last Updated on: 11th Jan 2023
 */
----
-- 1. Table `visitors`
----
CREATE TABLE IF NOT EXISTS `visitors`(
    `Id` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `Ip` VARCHAR(20) NOT NULL UNIQUE,
    `Username` VARCHAR(30) DEFAULT NULL,
    `LastVisited` DATETIME NOT NULL,
    `VisitCount` SMALLINT UNSIGNED DEFAULT 0
);

----
-- First execute above query then run below query because of foreign key constraint.
-- 2. Table `ip_info`
----
CREATE TABLE IF NOT EXISTS `ip_info`(
    `Id` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `Pin` VARCHAR(10) NOT NULL,
    `City` VARCHAR(30) NOT NULL,
    `State` VARCHAR(30) NOT NULL,
    `Country` VARCHAR(30) NOT NULL,
    `Isp` VARCHAR(50) NOT NULL,
    `TimeZone` VARCHAR(50) NOT NULL,
    FOREIGN KEY(Id) REFERENCES visitors(Id)
);

----
-- 3. Table `visitors_info`
----
CREATE TABLE IF NOT EXISTS `visitors_info`(
    `Id` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `Platform` VARCHAR(30) DEFAULT NULL,
    `Screen` VARCHAR(20) DEFAULT NULL,
    `Path` VARCHAR(50) NOT NULL,
    `Referrer` VARCHAR(200) DEFAULT NULL,
    FOREIGN KEY(Id) REFERENCES visitors(Id)
);