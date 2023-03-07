/*
 * MySQL
 * Schema for database `app` or `rdsbca$app`.
 * Created by: Suraj Kumar Giri
 * Created on: 7th March 2023
 * Last updated 7th March 2023
 */
----
-- 1. Table `otp_records`
----
CREATE TABLE IF NOT EXISTS `otp_records` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `OtpId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `Email` VARCHAR(100) NOT NULL,
    /*use 7 digits or less for otp (for MEDIUMINT)*/
    `Otp` MEDIUMINT UNSIGNED NOT NULL,
    `GeneratedOn` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `ExpireOn` DATETIME DEFAULT NULL,
);

----
-- 2. Table `otp_archive`
----
CREATE TABLE IF NOT EXISTS `otp_archive` (
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `OtpId` INT UNSIGNED NOT NULL,
    `Email` VARCHAR(100) NOT NULL,
    `Otp` MEDIUMINT UNSIGNED NOT NULL,
    `GeneratedOn` DATETIME DEFAULT NULL,
    `ExpireOn` DATETIME DEFAULT NULL,
);