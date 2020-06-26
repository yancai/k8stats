-- 容器统计信息表
CREATE TABLE `k8s_stats`.`kt_container_stats` (
  `id`          INT(11) NOT NULL AUTO_INCREMENT,
  `batch`       VARCHAR(255) NOT NULL,
  `cluster`     VARCHAR(255) NULL,
  `node`        VARCHAR(255) NOT NULL,
  `namespace`   VARCHAR(255) NOT NULL,
  `pod`         VARCHAR(255) NOT NULL,
  `container`   VARCHAR(255) NOT NULL,
  `cpu_request` BIGINT NULL,
  `cpu_limit`   BIGINT NULL,
  `cpu_used`    BIGINT NULL,
  `mem_request` BIGINT NULL,
  `mem_limit`   BIGINT NULL,
  `mem_used`    BIGINT NULL,
  `sample_time` INT NULL,
  PRIMARY KEY (`id`));

-- 容器统计信息视图，增加百分比
CREATE VIEW `k8s_stats`.`v_container_stats` AS
  SELECT `id`                           AS `id`,
         `batch`                        AS `batch`,
         `cluster`                      AS `cluster`,
         `node`                         AS `node`,
         `namespace`                    AS `namespace`,
         `pod`                          AS `pod`,
         `container`                    AS `container`,
         `cpu_request`                  AS `cpu_request`,
         `cpu_limit`                    AS `cpu_limit`,
         `cpu_used`                     AS `cpu_used`,
         (`cpu_used` / `cpu_request`)   AS `cpu_used_percent`,
         `mem_request`                  AS `mem_request`,
         `mem_limit`                    AS `mem_limit`,
         `mem_used`                     AS `mem_used`,
         (`mem_used` / `mem_request`)   AS `mem_used_percent`,
         `sample_time`                  AS `sample_time`
  FROM `k8s_stats`.`kt_container_stats`
