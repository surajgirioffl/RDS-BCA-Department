/*
 * MySQL
 * Schema for database `block_list` or `rdsbca$block_list`.
 * Created by: Suraj Kumar Giri
 * Created on: 6th March 2023
 * Last updated 7th March 2023
 */
CREATE TABLE IF NOT EXISTS `user_blocklist`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `BlockId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `UserId` INT UNSIGNED NOT NULL,
    `BlockedOn` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `BlockedBy` VARCHAR(50) NOT NULL,
    `BlockReason` VARCHAR(500) NOT NULL,
    `UnblockedOn` DATETIME DEFAULT NULL,
    `UnblockedBy` VARCHAR(50) DEFAULT NULL
    /*BlockedBy & UnblockedBy - username or person/moderator/adminstrator who blocked the user*/
);

CREATE TABLE IF NOT EXISTS `ip_blocklist`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `BlockId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `Ip` VARCHAR(20) NOT NULL,
    `BlockedOn` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `BlockedBy` VARCHAR(50) NOT NULL,
    `BlockReason` VARCHAR(500) NOT NULL,
    `UnblockedOn` DATETIME DEFAULT NULL,
    `UnblockedBy` VARCHAR(50) DEFAULT NULL
    /*BlockedBy & UnblockedBy - username or person/moderator/adminstrator who blocked the user*/
);

CREATE TABLE IF NOT EXISTS `blocked_users_archive`(
    `SNo` SMALLINT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    `BlockId` INT UNSIGNED PRIMARY KEY NOT NULL,
    `UserId` INT UNSIGNED NOT NULL,
    `BlockedOn` DATETIME NOT NULL,
    `BlockedBy` VARCHAR(50) NOT NULL,
    `BlockReason` VARCHAR(500) NOT NULL,
    `UnblockedOn` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `UnblockedBy` VARCHAR(50) NOT NULL,
    FOREIGN KEY (`BlockId`) REFERENCES user_blocklist(BlockId)
    /*BlockedBy & UnblockedBy - username or person/moderator/adminstrator who blocked the user*/
);