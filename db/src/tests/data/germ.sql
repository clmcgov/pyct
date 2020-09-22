insert into germ_test
    (template, start_date)
values
    (False, '1-1-2000');

insert into germ_moisture 
values
    ('H2O');


insert into germ_substrate 
values
    ('paper');


insert into germ_treatment
    (test_id, control, start_day, moisture, substrate, day_length, day_light, day_temp, night_temp)
values
    (1, false, 10, 'H2O', 'paper', 24, 1, 1, null, null),   --1
    (1, false, 11, 'H2O', 'paper', 12, 2, 2, 3, 3),         --2
    (1, false, 12, 'H2O', 'paper', 12, 3, 3, 4, 4),         --3
    (1, false, 13, 'H2O', 'paper', 12, 5, 5, 6, 6),         --4
    (1, false, 13, 'H2O', 'paper', 24, 7, 7, null, null),   --5
    (1, true, 11, 'H2O', 'paper', 23, 8, 8, 9, 9);          --6


insert into germ_inventory
    (inventory_id, treatment_id, seed_number)
values
    (1, 1, 5),
    (2, 1, 5);


insert into germ_transfer
    (test_id, source_id, target_id, seed_number)
values
    (1, 1, 2, 5),
    (1, 2, 3, 4),
    (1, 2, 4, 1),
    (1, 3, 5, 0);


insert into germ_count
    (treatment_id, count_day, germinated)
values
    (1, 11, 4);
