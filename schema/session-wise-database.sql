/*
 * MySQL
 * Schema for database of different sessions like `2020-23`, `2021-24`, ... or `rdsbca$2020-23', `rdsbca$2021-24`, `rdsbca$2022-25`, ...
 * Created by: Suraj Kumar Giri
 * Created on: 9th Jan 2023
 * Last updated on: 10th Jan 2023
 */
----
-- 1. Table `Students` 
----
CREATE TABLE `Students` (
    `SNo` TINYINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `RegistrationNo` VARCHAR(50) PRIMARY KEY NOT NULL,
    `ExamRoll` MEDIUMINT UNIQUE NOT NULL,
    `ClassRoll` TINYINT UNIQUE NOT NULL,
    `Name` VARCHAR(50) NOT NULL,
    `Gender` VARCHAR(10) NOT NULL DEFAULT 'Male'
);

-- First execute above query then run below query because of foreign key constraint.
----
-- 2. Table `Contact` 
----
CREATE TABLE `Contact` (
    `SNo` TINYINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `RegistrationNo` VARCHAR(50) PRIMARY KEY NOT NULL,
    `Email` VARCHAR(100) UNIQUE NOT NULL,
    `PhoneNo` VARCHAR(15) UNIQUE,
    `City` VARCHAR(30),
    FOREIGN KEY(RegistrationNo) REFERENCES Students(RegistrationNo)
);

----
-- You can use this table schema to create table for result of all semesters. Like 'ResultSem2', 'ResultSem3', ... 
-- 3. Table `ResultSem1`
----
CREATE TABLE `ResultSem1`(
    `SNo` TINYINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `RegistrationNo` VARCHAR(50) PRIMARY KEY NOT NULL,
    `ExamRoll` MEDIUMINT UNIQUE NOT NULL,
    `TotalMarks` SMALLINT NOT NULL,
    `ResultStatus` VARCHAR(100) NOT NULL DEFAULT 'Pass',
    `MoreInfo` VARCHAR(200),
    FOREIGN KEY(RegistrationNo) REFERENCES Students(RegistrationNo)
);