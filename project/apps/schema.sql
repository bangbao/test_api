-- 全局sql文件
-- 执行后可创建项目全部的表，主要用于新项目部署

CREATE TABLE `user_data` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `token` varchar(255) NOT NULL DEFAULT '',
       `username` varchar(255) NOT NULL DEFAULT '',
       `salt` char(10) NOT NULL DEFAULT '',
       `password` char(40) NOT NULL DEFAULT '',
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`),
       UNIQUE (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `game_info` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `username` varchar(255) NOT NULL DEFAULT '',
       `enter` BOOLEAN DEFAULT false,
       `role` TINYINT unsigned NOT NULL DEFAULT 0,
       `vip` SMALLINT unsigned NOT NULL DEFAULT 0,
       `equip` SMALLINT unsigned NOT NULL DEFAULT 0,
       `hero` SMALLINT unsigned NOT NULL DEFAULT 0,
       `exp` MEDIUMINT unsigned NOT NULL DEFAULT 0,
       `energy` TINYINT unsigned NOT NULL DEFAULT 0,
       `cost` TINYINT unsigned NOT NULL DEFAULT 0,
       `friend` TINYINT unsigned NOT NULL DEFAULT 0,
       `energy_fill_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `game_user` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `level` SMALLINT unsigned NOT NULL DEFAULT 0,
       `exp` MEDIUMINT unsigned NOT NULL DEFAULT 0,
       `light` SMALLINT unsigned NOT NULL DEFAULT 0,
       `dark` SMALLINT unsigned NOT NULL DEFAULT 0,
       `kcoin` SMALLINT unsigned NOT NULL DEFAULT 0,
       `gold` int(11) unsigned NOT NULL DEFAULT 0,
       `energy` TINYINT unsigned NOT NULL DEFAULT 0,
       `battle` TINYINT unsigned NOT NULL DEFAULT 0,
       `team` varchar(255) DEFAULT '',
       `pet` varchar(255) DEFAULT '',
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `game_equip` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `pos0` varchar(255) DEFAULT '',
       `pos1` varchar(255) DEFAULT '',
       `pos2` varchar(255) DEFAULT '',
       `pos3` varchar(255) DEFAULT '',
       `pos4` varchar(255) DEFAULT '',
       `pos5` varchar(255) DEFAULT '',
       `pos6` varchar(255) DEFAULT '',
       `pos7` varchar(255) DEFAULT '',
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `game_goblin` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `pos0` varchar(255) DEFAULT '',
       `pos1` varchar(255) DEFAULT '',
       `pos2` varchar(255) DEFAULT '',
       `pos3` varchar(255) DEFAULT '',
       `pos4` varchar(255) DEFAULT '',
       `pos5` varchar(255) DEFAULT '',
       `pos6` varchar(255) DEFAULT '',
       `pos7` varchar(255) DEFAULT '',
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `game_config` (
  `id` varchar(255) NOT NULL,
  `value` longtext NOT NULL,
  `env` varchar(255) DEFAULT '',
  `ver` varchar(255) DEFAULT '',
  `name` varchar(255) DEFAULT '',
  `created_at` int(10) unsigned NOT NULL DEFAULT '0',
  `updated_at` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

create table `game_friends` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(11) unsigned NOT NULL DEFAULT '0',
  `fid` int(11) unsigned NOT NULL DEFAULT '0',
  `foreign_at` varchar(255) NOT NULL DEFAULT '',
  `created_at` int(10) unsigned NOT NULL DEFAULT '0',
  `updated_at` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) engine=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `hero_heros` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `hero_id` varchar(255) DEFAULT '',
       `uid` int(11) unsigned NOT NULL DEFAULT '0',
       `cfg_id` int(11) unsigned NOT NULL DEFAULT 0,
       `level` SMALLINT unsigned NOT NULL DEFAULT 0,
       `exp` MEDIUMINT unsigned NOT NULL DEFAULT 0,
       `level_up` MEDIUMINT unsigned NOT NULL DEFAULT 0,
       `job` TINYINT unsigned NOT NULL DEFAULT 0,
       `hp` MEDIUMINT unsigned NOT NULL DEFAULT 0,
       `natk` SMALLINT unsigned NOT NULL DEFAULT 0,
       `ndef` SMALLINT unsigned NOT NULL DEFAULT 0,
       `matk` SMALLINT unsigned NOT NULL DEFAULT 0,
       `mdef` SMALLINT unsigned NOT NULL DEFAULT 0,
       `cost` TINYINT unsigned NOT NULL DEFAULT 0,
       `askill` SMALLINT unsigned NOT NULL DEFAULT 0,
       `nskill` SMALLINT unsigned NOT NULL DEFAULT 0,
       `lock` BOOLEAN DEFAULT false,
       `sign` char(40) DEFAULT '',
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`),
       UNIQUE (`hero_id`),
       KEY(`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `hero_data` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `resolve` SMALLINT unsigned NOT NULL DEFAULT 0,
       `resolve_top` SMALLINT unsigned NOT NULL DEFAULT 0,
       `st_cd` TINYINT unsigned NOT NULL DEFAULT 0,
       `st_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `last_date` char(10) DEFAULT '',
       `forge` SMALLINT unsigned NOT NULL DEFAULT 0,
       `forge_cycle` TINYINT unsigned NOT NULL DEFAULT 0,
       `forge_point` SMALLINT unsigned NOT NULL DEFAULT 0,
       `forge_level` TINYINT unsigned NOT NULL DEFAULT 0,
       `masters` char(10) DEFAULT '',
       `master_at` char(20) DEFAULT '',
       `master_up` TINYINT unsigned NOT NULL DEFAULT 0,
       `pet_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `pet_skill` TINYINT unsigned NOT NULL DEFAULT 0,
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `hero_equips` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `equip_id` varchar(255) DEFAULT '',
       `uid` int(11) unsigned NOT NULL DEFAULT '0',
       `cfg_id` int(11) unsigned NOT NULL DEFAULT 0,
       `level` SMALLINT unsigned NOT NULL DEFAULT 0,
       `hp` MEDIUMINT unsigned NOT NULL DEFAULT 0,
       `natk` SMALLINT unsigned NOT NULL DEFAULT 0,
       `ndef` SMALLINT unsigned NOT NULL DEFAULT 0,
       `matk` SMALLINT unsigned NOT NULL DEFAULT 0,
       `mdef` SMALLINT unsigned NOT NULL DEFAULT 0,
       `gold` int(11) unsigned NOT NULL DEFAULT 0,
       `sign` char(40) DEFAULT '',
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`),
       UNIQUE (`equip_id`),
       KEY(`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `hero_materials` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `cfg_id` int(11) unsigned NOT NULL DEFAULT 0,
       `uid` int(11) unsigned NOT NULL DEFAULT '0',
       `num` SMALLINT unsigned NOT NULL DEFAULT 0,
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`),
       KEY(`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `hero_items` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `cfg_id` int(11) unsigned NOT NULL DEFAULT 0,
       `uid` int(11) unsigned NOT NULL DEFAULT '0',
       `num` SMALLINT unsigned NOT NULL DEFAULT 0,
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`),
       KEY(`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `hero_goblins` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `goblin_id` varchar(255) DEFAULT '',
       `uid` int(11) unsigned NOT NULL DEFAULT '0',
       `cfg_id` int(11) unsigned NOT NULL DEFAULT 0,
       `level` SMALLINT unsigned NOT NULL DEFAULT 0,
       `exp` MEDIUMINT unsigned NOT NULL DEFAULT 0,
       `level_up` MEDIUMINT unsigned NOT NULL DEFAULT 0,
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`),
       UNIQUE (`goblin_id`),
       KEY(`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `hero_pets` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `pet_id` varchar(255) DEFAULT '',
       `uid` int(11) unsigned NOT NULL DEFAULT '0',
       `cfg_id` int(11) unsigned NOT NULL DEFAULT 0,
       `level` SMALLINT unsigned NOT NULL DEFAULT 0,
       `exp` MEDIUMINT unsigned NOT NULL DEFAULT 0,
       `level_up` MEDIUMINT unsigned NOT NULL DEFAULT 0,
       `hp` MEDIUMINT unsigned NOT NULL DEFAULT 0,
       `natk` SMALLINT unsigned NOT NULL DEFAULT 0,
       `ndef` SMALLINT unsigned NOT NULL DEFAULT 0,
       `matk` SMALLINT unsigned NOT NULL DEFAULT 0,
       `mdef` SMALLINT unsigned NOT NULL DEFAULT 0,
       `full` SMALLINT unsigned NOT NULL DEFAULT 0,
       `clone` TINYINT unsigned NOT NULL DEFAULT 0,
       `skill` varchar(255) DEFAULT '',
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`),
       UNIQUE (`pet_id`),
       KEY(`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `adven_adven` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `chapter` SMALLINT unsigned NOT NULL DEFAULT 0,
       `stage` MEDIUMINT unsigned NOT NULL DEFAULT 0,
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `adven_readven` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `uid` SMALLINT unsigned NOT NULL DEFAULT 0,
       `chapter` SMALLINT unsigned NOT NULL DEFAULT 0,
       `stage` MEDIUMINT unsigned NOT NULL DEFAULT 0,
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`),
       KEY(`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `adven_data` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `uid` SMALLINT unsigned NOT NULL DEFAULT 0,
       `stage` MEDIUMINT unsigned NOT NULL DEFAULT 0,
       `light` SMALLINT unsigned NOT NULL DEFAULT 0,
       `dark` SMALLINT unsigned NOT NULL DEFAULT 0,
       `grade` TINYINT unsigned NOT NULL DEFAULT 0,
       `energy` TINYINT unsigned NOT NULL DEFAULT 0,
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`),
       KEY(`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `arena_data` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `buy_count` TINYINT unsigned NOT NULL DEFAULT 0,
       `battle` TINYINT unsigned NOT NULL DEFAULT 0,
       `battle_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `refresh` TINYINT unsigned NOT NULL DEFAULT 0,
       `rivals` varchar(255) DEFAULT '',
       `last_date` char(20) DEFAULT '',
       `award_at` char(20) DEFAULT '',
       `per_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `cont_win` TINYINT UNSIGNED NOT NULL DEFAULT 0,
       `score` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `rank` SMALLINT unsigned NOT NULL DEFAULT 0,
       `rank_score` char(20) DEFAULT '',
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `arena_logs` (
       `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
       `log_id` varchar(255) DEFAULT '',
       `uid` int(11) unsigned NOT NULL DEFAULT '0',
       `ts` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `type` char(6) DEFAULT '',
       `win` BOOLEAN DEFAULT false,
       `target_id` int(11) unsigned NOT NULL DEFAULT '0',
       `target_name` varchar(255) DEFAULT '',
       `change_rank` SMALLINT unsigned NOT NULL DEFAULT 0,
       `created_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       `updated_at` int(10) UNSIGNED NOT NULL DEFAULT 0,
       PRIMARY KEY (`id`),
       UNIQUE (`log_id`),
       KEY(`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;