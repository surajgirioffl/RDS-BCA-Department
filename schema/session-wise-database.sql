/*
 * MySQL
 * Schema for database of different sessions like `2020-23`, `2021-24`, ... or `rdsbca$2020-23`, `rdsbca$2021-24`, `rdsbca$2022-25`, ...
 * Created by: Suraj Kumar Giri
 * Created on: 9th Jan 2023
 * Last updated on: 8th Feb 2023
 */
----
-- 1. Table `students` 
----
CREATE TABLE IF NOT EXISTS `students` (
    `SNo` TINYINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `RegistrationNo` VARCHAR(50) PRIMARY KEY NOT NULL,
    `ExamRoll` MEDIUMINT UNIQUE NOT NULL,
    `ClassRoll` TINYINT UNIQUE NOT NULL,
    `Name` VARCHAR(50) NOT NULL,
    `Gender` ENUM('Male', 'Female', 'Others') NOT NULL DEFAULT 'Male'
);

-- First execute above query then run below query because of foreign key constraint.
----
-- 2. Table `contact` 
----
CREATE TABLE IF NOT EXISTS `contact` (
    `SNo` TINYINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `RegistrationNo` VARCHAR(50) PRIMARY KEY NOT NULL,
    `Email` VARCHAR(100) UNIQUE NOT NULL,
    `PhoneNo` VARCHAR(15) UNIQUE DEFAULT NULL,
    `City` VARCHAR(30) DEFAULT NULL,
    FOREIGN KEY(RegistrationNo) REFERENCES Students(RegistrationNo)
);

----
-- You can use this table schema to create table for result of all semesters. Like 'result_sem1', 'result_sem2', 'result_sem3', ... 
-- 3. Table `result_sem1`
----
CREATE TABLE IF NOT EXISTS `result_sem1`(
    `SNo` TINYINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `RegistrationNo` VARCHAR(50) PRIMARY KEY NOT NULL,
    `ExamRoll` MEDIUMINT UNIQUE NOT NULL,
    `TotalMarks` SMALLINT NOT NULL,
    `ResultStatus` VARCHAR(100) NOT NULL DEFAULT 'Pass',
    `MoreInfo` VARCHAR(200) DEFAULT NULL,
    FOREIGN KEY(RegistrationNo) REFERENCES Students(RegistrationNo)
);

----
-- You can use this table schema to create table for subject wise marks of all semesters. Like 'subject_wise_marks_sem1', 'subject_wise_marks_sem2', ...
-- Must change subject code to subject code for respective semesters. Example: for sem3, it will 301, 302 and so on till 306.
-- 4. Table `subject_wise_marks_sem1`
-- Subject wise result for bca semester system published by the University on 17th Feb 2022. And may be in future the same will continue.
----
CREATE TABLE IF NOT EXISTS `subject_wise_marks_sem1`(
    `SNo` TINYINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `RegistrationNo` VARCHAR(50) PRIMARY KEY NOT NULL,
    `ExamRoll` MEDIUMINT UNIQUE NOT NULL,
    `101` VARCHAR(15) DEFAULT NULL,
    `102` VARCHAR(15) DEFAULT NULL,
    `103` VARCHAR(15) DEFAULT NULL,
    `104` VARCHAR(15) DEFAULT NULL,
    `105` VARCHAR(15) DEFAULT NULL,
    `106` VARCHAR(15) DEFAULT NULL,
    FOREIGN KEY(RegistrationNo) REFERENCES Students(RegistrationNo)
);