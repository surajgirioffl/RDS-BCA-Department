/*
 * MySQL
 * Schema for database `Bca` or `rdsbca$Bca`
 * Created by: Suraj Kumar Giri
 * Created on: 7th Jan 2023
 */
----
-- 1. Table `Students`
----
CREATE TABLE Students(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `RegistrationNo` CHAR(100) PRIMARY KEY NOT NULL,
    `Session` CHAR(10) NOT NULL
);

----
-- 2. Table `Teachers`
----
CREATE TABLE Teachers(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `TeacherId` CHAR(100) PRIMARY KEY NOT NULL,
    `Name` CHAR(100) NOT NULL,
    `Subjects` CHAR(255) NOT NULL,
    `PhoneNo` CHAR(15) UNIQUE,
    `Email` CHAR(100) UNIQUE,
    `SocialLink` CHAR(200) UNIQUE
);

----
-- 3. Table `Subjects `
----
CREATE TABLE `Subjects`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `SubjectCode` SMALLINT UNSIGNED PRIMARY KEY NOT NULL,
    `SubjectCodeChar` CHAR(10) NOT NULL UNIQUE,
    `SubjectTitle` CHAR(255) NOT NULL UNIQUE,
    `Semester` TINYINT UNSIGNED NOT NULL,
    `InternalMarks` TINYINT UNSIGNED NOT NULL default 20,
    `ExternalMarks` TINYINT UNSIGNED NOT NULL default 80,
    `TotalMarks` TINYINT UNSIGNED NOT NULL default 100
);