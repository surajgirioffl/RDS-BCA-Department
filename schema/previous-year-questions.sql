/*
 * MySQL
 * Schema for database `previous_year_questions` or `rdsbca$previous_year_questions`.
 * Created by: Suraj Kumar Giri
 * Created on: 8th Jan 2023
 * Last updated on: 13th April 2023
 */
----
-- 1. Table `brabu` 
----
CREATE TABLE IF NOT EXISTS `brabu`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `Year` SMALLINT UNSIGNED PRIMARY KEY NOT NULL,
    `Sem1` INT UNSIGNED UNIQUE,
    `Sem2` INT UNSIGNED UNIQUE,
    `Sem3` INT UNSIGNED UNIQUE,
    `Sem4` INT UNSIGNED UNIQUE,
    `Sem5` INT UNSIGNED UNIQUE
);

----
-- 2. Table `ln_mishra` 
----
CREATE TABLE IF NOT EXISTS `ln_mishra`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `Year` SMALLINT UNSIGNED PRIMARY KEY NOT NULL,
    `Sem1` INT UNSIGNED UNIQUE,
    `Sem2` INT UNSIGNED UNIQUE,
    `Sem3` INT UNSIGNED UNIQUE,
    `Sem4` INT UNSIGNED UNIQUE,
    `Sem5` INT UNSIGNED UNIQUE
);

----
-- 3. Table `vaishali` 
----
CREATE TABLE IF NOT EXISTS `vaishali`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `Year` SMALLINT UNSIGNED PRIMARY KEY NOT NULL,
    `Sem1` INT UNSIGNED UNIQUE,
    `Sem2` INT UNSIGNED UNIQUE,
    `Sem3` INT UNSIGNED UNIQUE,
    `Sem4` INT UNSIGNED UNIQUE,
    `Sem5` INT UNSIGNED UNIQUE
);