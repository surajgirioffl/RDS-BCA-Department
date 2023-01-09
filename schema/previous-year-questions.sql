/*
 * MySQL
 * Schema for database `PreviousYearQuestions` or `rdsbca$PreviousYearQuestions`.
 * Created by: Suraj Kumar Giri
 * Created on: 8th Jan 2023
 */
----
-- 1. Table `Brabu` 
----
CREATE TABLE `Brabu`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `Year` SMALLINT UNSIGNED PRIMARY KEY NOT NULL,
    `Sem1` MEDIUMINT UNSIGNED UNIQUE,
    `Sem2` MEDIUMINT UNSIGNED UNIQUE,
    `Sem3` MEDIUMINT UNSIGNED UNIQUE,
    `Sem4` MEDIUMINT UNSIGNED UNIQUE,
    `Sem5` MEDIUMINT UNSIGNED UNIQUE
);