/*
 * MySQL
 * Schema for database `users` or `rdsbca$users`.
 * Created by: Suraj Kumar Giri
 * Created on: 6th March 2023
 * Last updated 7th March 2023
 */
----
-- 1. Table `users`
----
CREATE TABLE IF NOT EXISTS `users`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `UserId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `Username` VARCHAR(50) UNIQUE NOT NULL,
    `Password` VARCHAR(100) NOT NULL,
);

----
-- 2. Table `users_info`
----
CREATE TABLE IF NOT EXISTS `users_info`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `UserId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `FirstName` VARCHAR(50) NOT NULL,
    `LastName` VARCHAR(50) NOT NULL,
    `Email` VARCHAR(100) UNIQUE NOT NULL,
    `PhoneNo` VARCHAR(15) UNIQUE DEFAULT NULL,
    `Gender` ENUM('Male', 'Female') NOT NULL,
    `RegistrationNo` VARCHAR(50) UNIQUE NOT NULL,
    `Session` VARCHAR(10) NOT NULL,
    FOREIGN KEY (`UserId`) REFERENCES users(`UserId`) ON DELETE CASCADE
);

----
-- 3. Table `user_statistics`
----
CREATE TABLE IF NOT EXISTS `user_statistics`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `UserId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `LastVisited` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `VisitCount` SMALLINT UNSIGNED DEFAULT 0,
    `RegisteredOn` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ('UserId') REFERENCES users('UserId')
);