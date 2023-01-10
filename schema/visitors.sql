/*
 * MySQL
 * Schema for database `visitors` or `rdsbca$visitors`
 * Created by: Suraj Kumar Giri
 * Created on: 10th Jan 2023
 * Last Updated on: 10th Jan 2023
 */
----
-- 1. Table `visitors`
----
CREATE TABLE IF NOT EXISTS `visitors`(
    `Id` MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `Ip` VARCHAR(20) NOT NULL UNIQUE,
    `LastVisited` DATETIME NOT NULL,
    `VisitCount` SMALLINT UNSIGNED DEFAULT 0
);