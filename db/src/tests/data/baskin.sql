insert into germ_test
    (description)
values
    ('Baskin & Baskin, 1999');  --1


insert into germ_moisture 
    (name, description)
values
    ('H2O', 'tap water');   --1


insert into germ_substrate
    (name, description)
values
    ('paper', 'petri dishes with filter paper');    --1


insert into germ_light
    (name, description)
values
    ('cool white', 'fluorescent light (irradiance equal to about 2% of visible portion of full sunlight in summer)');   --1


insert into germ_treatment
    (test_id, control, start_day, moisture, substrate, day_length, day_light, day_temp, night_temp, description)
values
    -- control
    (1, true, 0, 'H2O', 'paper', 24, 'cool white', 5, null, 'control - winter'),        --1
    (1, true, 0, 'H2O', 'paper', 12, 'cool white', 15, 6, 'control - early spring'),    --2
    (1, true, 0, 'H2O', 'paper', 12, 'cool white', 20, 10, 'control - late spring'),    --3
    (1, true, 0, 'H2O', 'paper', 12, 'cool white', 25, 15, 'control - summer'),         --4
    -- winter start
    (1, false, 0, 'H2O', 'paper', 24, 'cool white', 5, null, 'winter - winter'),         --5
    (1, false, 28, 'H2O', 'paper', 12, 'cool white', 15, 6, 'winter - early spring'),    --6
    (1, false, 56, 'H2O', 'paper', 12, 'cool white', 20, 10, 'winter - late spring'),    --7
    (1, false, 84, 'H2O', 'paper', 12, 'cool white', 25, 15, 'winter - summer'),         --8
    (1, false, 112, 'H2O', 'paper', 12, 'cool white', 20, 10, 'winter - early autumn'),  --9
    (1, false, 140, 'H2O', 'paper', 12, 'cool white', 15, 6, 'winter - late autumn'),    --10
    -- summer start
    (1, false, 0, 'H2O', 'paper', 12, 'cool white', 25, 15, 'summer - summer'),          --11
    (1, false, 28, 'H2O', 'paper', 12, 'cool white', 20, 10, 'summer - early autumn'),   --12
    (1, false, 56, 'H2O', 'paper', 12, 'cool white', 15, 6, 'summer - late autumn'),     --13
    (1, false, 84, 'H2O', 'paper', 24, 'cool white', 5, null, 'summer - winter'),        --14
    (1, false, 112, 'H2O', 'paper', 12, 'cool white', 15, 6, 'summer - early spring'),   --15
    (1, false, 140, 'H2O', 'paper', 12, 'cool white', 20, 10, 'summer - late spring');   --16


insert into germ_inventory
    (inventory_id, treatment_id, seed_number)
values
    -- control
    (1, 1, 50),
    (1, 2, 50),
    (1, 3, 50),
    (1, 4, 50),
    -- winter start
    (1, 5, 50),
    -- summer start
    (1, 11, 50);


insert into germ_transfer
    (test_id, source_id, target_id, seed_number)
values
    -- winter start
    (1, 5, 6, 50),
    (1, 6, 7, 50),
    (1, 7, 8, 50),
    (1, 8, 9, 50),
    (1, 9, 10, 50),
    -- summer start
    (1, 11, 12, 50),
    (1, 12, 13, 50),
    (1, 13, 14, 50),
    (1, 14, 15, 50),
    (1, 15, 16, 50);


insert into germ_count
    (treatment_id, count_day)
values
    -- winter control
    (1, 14),
    (1, 28),
    (1, 42),
    (1, 56),
    (1, 70),
    (1, 84),
    (1, 98),
    (1, 112),
    (1, 126),
    (1, 140),
    (1, 154),
    (1, 168),
    -- early spring control
    (2, 14),
    (2, 28),
    (2, 42),
    (2, 56),
    (2, 70),
    (2, 84),
    (2, 98),
    (2, 112),
    (2, 126),
    (2, 140),
    (2, 154),
    (2, 168),
    -- late spring control
    (3, 14),
    (3, 28),
    (3, 42),
    (3, 56),
    (3, 70),
    (3, 84),
    (3, 98),
    (3, 112),
    (3, 126),
    (3, 140),
    (3, 154),
    (3, 168),
    -- summer control
    (4, 14),
    (4, 28),
    (4, 42),
    (4, 56),
    (4, 70),
    (4, 84),
    (4, 98),
    (4, 112),
    (4, 126),
    (4, 140),
    (4, 154),
    (4, 168),
    -- winter start
    (5, 14),
    (5, 28),
    (6, 42),
    (6, 56),
    (7, 70),
    (7, 84),
    (8, 98),
    (8, 112),
    (9, 126),
    (9, 140),
    (10, 154),
    (10, 168),
    -- summer start
    (11, 14),
    (11, 28),
    (12, 42),
    (12, 56),
    (13, 70),
    (13, 84),
    (14, 98),
    (14, 112),
    (15, 126),
    (15, 140),
    (16, 154),
    (16, 168);