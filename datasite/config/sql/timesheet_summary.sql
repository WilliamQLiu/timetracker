CREATE
    ALGORITHM = UNDEFINED
    DEFINER = `root`@`localhost`
    SQL SECURITY DEFINER
VIEW `timesheet_summary` AS
    select
        `timesheets_time`.`id` AS `time_id`,
        `timesheets_time`.`date_select` AS `date_select`,
        `auth_user`.`username` AS `username`,
        `auth_user`.`email` AS `email`,
        `timesheets_costcode`.`program_name` AS `program_name`,
        `timesheets_costcode`.`cost_code` AS `cost_code`,
        `timesheets_program`.`hours_spent` AS `hours_spent`,
        `timesheets_program`.`minutes_spent` AS `minutes_spent`,
        `timesheets_program`.`notes` AS `notes`,
        ((ifnull(`timesheets_program`.`hours_spent`, 0) * 60) + ifnull(`timesheets_program`.`minutes_spent`, 0)) AS `total_minutes`
    from
        (((`timesheets_time`
        join `timesheets_program` ON ((`timesheets_time`.`id` = `timesheets_program`.`time_id`)))
        join `auth_user` ON ((`timesheets_time`.`user_id` = `auth_user`.`id`)))
        join `timesheets_costcode` ON ((`timesheets_costcode`.`id` = `timesheets_program`.`program_select_id`)))
