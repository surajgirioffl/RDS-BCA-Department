/*
 * MySQL
 * Schema for database `bca` or `rdsbca$bca`
 * Created by: Suraj Kumar Giri
 * Created on: 7th Jan 2023
 * Last Updated on: 11th Feb 2023
 */
----
-- 1. Table `students`
----
CREATE TABLE IF NOT EXISTS students(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `RegistrationNo` VARCHAR(50) PRIMARY KEY NOT NULL,
    `Session` VARCHAR(10) NOT NULL
);

----
-- 2. Table `subjects `
----
CREATE TABLE IF NOT EXISTS `subjects`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `SubjectCode` SMALLINT UNSIGNED PRIMARY KEY NOT NULL,
    `SubjectCodeChar` CHAR(7) NOT NULL UNIQUE,
    `SubjectTitle` VARCHAR(255) NOT NULL UNIQUE,
    `Semester` TINYINT UNSIGNED NOT NULL,
    `InternalMarks` TINYINT UNSIGNED NOT NULL default 20,
    `ExternalMarks` TINYINT UNSIGNED NOT NULL default 80,
    `TotalMarks` TINYINT UNSIGNED NOT NULL default 100
);