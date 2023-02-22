CREATE SCHEMA `hour_tracker` ;

CREATE TABLE `student` (
  `id_user` int unsigned NOT NULL,
  `name` char(50) NOT NULL,
  `second_name` char(50) NOT NULL,
  `objective_hours` float unsigned NOT NULL,
  `current_hours` float unsigned NOT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `register` (
  `id_register` int unsigned NOT NULL AUTO_INCREMENT,
  `fk_id_user` int unsigned NOT NULL,
  `enter_hour` datetime NOT NULL,
  `exit_hour` datetime NOT NULL,
  PRIMARY KEY (`id_register`),
  KEY `ForeignKey_id_user_register_idx` (`fk_id_user`),
  CONSTRAINT `ForeignKey_id_user_register` FOREIGN KEY (`fk_id_user`) REFERENCES `student` (`id_user`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

create role teacher;

grant role_admin,create user,delete,insert,update,select on *.* to 'teacher';
