/*
 * MySQL
 * Schema for database `users` or `rdsbca$users`.
 * Created by: Suraj Kumar Giri
 * Created on: 6th March 2023
 * Last updated 7th March 2023
 */
CREATE TABLE IF NOT EXISTS `users`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `UserId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `Username` VARCHAR(50) UNIQUE NOT NULL,
    `Password` VARCHAR(100) NOT NULL,
);