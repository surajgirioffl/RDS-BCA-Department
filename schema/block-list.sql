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