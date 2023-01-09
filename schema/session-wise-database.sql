/*
 * MySQL
 * Schema for database of different sessions like `2020-23`, `2021-24`, ... or `rdsbca$2020-23', `rdsbca$2021-24`, `rdsbca$2022-25`, ...
 * Created by: Suraj Kumar Giri
 * Created on: 9th Jan 2023
 * Last updated on: 9th Jan 2023
 */
----
-- 1. Table `Students` 
----
CREATE TABLE `Students` (
    `SNo` TINYINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `RegistrationNo` CHAR(50) PRIMARY KEY NOT NULL,
    `ExamRoll` MEDIUMINT UNIQUE NOT NULL,
    `ClassRoll` TINYINT UNIQUE NOT NULL,
    `Name` CHAR(50) NOT NULL,
    `Gender` CHAR(10) NOT NULL DEFAULT 'Male',
);

-- First execute above query then run below query because of foreign key constraint.
----
-- 2. Table `Contact` 
----
CREATE TABLE `Contact` (
    `SNo` TINYINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `RegistrationNo` CHAR(50) PRIMARY KEY NOT NULL,
    `Email` CHAR(100) UNIQUE NOT NULL,
    `PhoneNo` CHAR(15) UNIQUE,
    `City` CHAR(30),
    FOREIGN KEY(RegistrationNo) REFERENCES Students(RegistrationNo)
);