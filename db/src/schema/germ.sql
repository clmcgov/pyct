/* make some triggers before, add conditions for firing
*/


-- germ_test --

drop table if exists germ_test cascade;

create table germ_test (
    
    id          int primary key generated always as identity,
    description varchar,
    start_date  date,

    check (description is null or length(trim(description)) > 0)
);



-- germ_moisture --

drop table if exists germ_moisture cascade;

create table germ_moisture (
    
    name        varchar primary key,
    description varchar,

    check (description is null or length(trim(description)) > 0)
);



-- germ_substrate --

drop table if exists germ_substrate cascade;

create table germ_substrate (
    
    name        varchar primary key,
    description varchar,

    check (description is null or length(trim(description)) > 0)
);



-- germ_light --

drop table if exists germ_light cascade;

create table germ_light (
    
    name        varchar primary key,
    description varchar,

    check (description is null or length(trim(description)) > 0)
);



-- germ_treatment --

drop table if exists germ_treatment cascade;

create table germ_treatment (
    
    id          int primary key generated always as identity,
    test_id     int not null,
    control     boolean not null default false,
    start_day   int not null,
    moisture    varchar not null,
    substrate   varchar not null,
    day_length  int not null default 24,
    day_light   varchar not null,
    day_temp    int not null,
    night_temp  int default null,
    description varchar,

    foreign key (test_id) references germ_test (id) on delete cascade,
    foreign key (moisture) references germ_moisture (name) on update cascade,
    foreign key (substrate) references germ_substrate (name) on update cascade,
    foreign key (day_light) references germ_light (name) on update cascade,

    unique (test_id, id),

    check (start_day >= 0),

    check (
        (
            day_length = 24
            and night_temp is null
        )
        or (
            day_length between 1 and 23
            and night_temp is not null
        )
    ),

    check (description is null or length(trim(description)) > 0)
);


drop function if exists after_germ_treatment_upd;

create function after_germ_treatment_upd ()
returns trigger
language plpgsql as $$

    begin
    -- no moving controls
    if new.control and exists (
        select *
        from germ_transfer
        where source_id = new.id
        or target_id = new.id
    )
    then raise 'controls may not particpate in transfers';
    -- check for source treatments that start on the same day as or before their target
    elsif exists (
        select *
        from germ_transfer as e
        join germ_treatment as s
        on e.source_id = s.id
        join germ_treatment as t
        on e.target_id = t.id
        where s.start_day >= t.start_day
        and (s.id = new.id or t.id = new.id)
    )
    then raise 'treatments may not start before preceding treatments';
    end if;

    return null;

    end;
$$;

create trigger after_upd
after update on germ_treatment
for each row execute procedure after_germ_treatment_upd();



-- germ_inventory --

drop table if exists germ_inventory cascade;

create table germ_inventory (

    inventory_id    int not null,
    treatment_id    int not null,
    seed_number      int not null default 0,

    primary key (inventory_id, treatment_id),

    foreign key (treatment_id) references germ_treatment (id) on delete cascade,

    check (seed_number >= 0)
);



-- germ_transfer --

drop table if exists germ_transfer cascade;

create table germ_transfer (

    test_id     integer not null,
    source_id   integer not null,
    target_id   integer not null,
    seed_number  integer not null default 0,

    primary key (source_id, target_id),

    foreign key (test_id, source_id) 
    references germ_treatment (test_id, id)
    on delete cascade,

    foreign key (test_id, target_id)
    references germ_treatment (test_id, id)
    on delete cascade,

    check (seed_number >= 0)
);


drop function if exists after_germ_transfer_op;

create function after_germ_transfer_op ()
returns trigger
language plpgsql as $$

    begin

    if tg_op in ('INSERT', 'UPDATE') then
        -- make sure we aren't transfering a control (should be before)
        if exists (
            select *
            from germ_treatment
            where id in (new.source_id, new.target_id)
            and control = true
        )
        then raise 'cannot transfer to or from control';
        -- see if we took more seeds than we had
        elsif exists (
            select *
            from germ_status(new.test_id)
            where available < 0
        )
        then raise 'cannot transfer more seeds than are available';
        -- see if we have a source treatment starting on the same day as or before the target
        elsif (
            (
                select start_day 
                from germ_treatment 
                where id = new.source_id
            ) >= (
                select start_day
                from germ_treatment
                where id = new.target_id
            )
        )
        then raise 'treatments may not start before preceding treatments';
        end if;
    elsif tg_op = 'DELETE' 
    and (
        select id::boolean
        from germ_status(old.test_id)
        where available < 0
    ) 
    then raise 'deletion results in treatments with more seeds than are available';
    
    end if;

    return new;

    end;
$$;

create trigger after_op
after insert or update or delete on germ_transfer
for each row execute procedure after_germ_transfer_op();


drop function if exists after_germ_transfer_del;

create function after_germ_transfer_del ()
returns trigger
language plpgsql as $$

    begin
 
    if (
        select id::boolean
        from germ_status(old.test_id)
        where available < 0
    ) 
    then raise 'deletion results in treatments with more seeds than are available';
    
    end if;

    return null;

    end;
$$;

create trigger after_del
after delete on germ_transfer
for each row execute procedure after_germ_transfer_del();



-- germ_count --

drop table if exists germ_count cascade;

create table germ_count (

    treatment_id    int not null,
    count_day       int not null,
    germinated      int not null default 0,
    discarded       int not null default 0,

    primary key (treatment_id, count_day),

    foreign key (treatment_id) 
    references germ_treatment (id)
    on delete cascade,

    check (germinated >= 0)
);


drop function if exists after_germ_count_ins_upd;

create function after_germ_count_ins_upd () 
returns trigger
language plpgsql as $$

    begin

    if exists (
        select *
        from germ_status(
            (select test_id from germ_treatment where id = new.treatment_id),
            new.count_day
        )
        where available < 0
    )
    then raise 'cannot count more germinated seeds than are available -- counts should not be cumulative';
    end if;

    return null;

    end;
$$;

create trigger after_ins_upd
after insert or update on germ_count
for each row execute procedure after_germ_count_ins_upd();


-- germ_total -- 


-- germ_result --

drop view if exists germ_result cascade;

create view germ_result as (
    
    select
        sub.id,
        sub.total,
        germ.germinated,
        (germ.germinated::real / sub.total::real) as viable
    from (
        select
            cnts.id,
            sum(cnts.cnt)::int as total
        from (
            -- seeds moved into treatment from other treatments
            select
                nt.id,
                sum(t.seed_number) as cnt
            from germ_treatment as nt
            join germ_transfer as t
            on t.target_id = nt.id
            group by nt.id 
            -- inventory seed sources  
            union select
                ni.id,
                sum(i.seed_number) as cnt
            from germ_treatment as ni
            join germ_inventory as i
            on i.treatment_id = ni.id
            group by ni.id
            -- seeds sent on to other treatments
            union select
                ns.id,
                -sum(s.seed_number) as cnt
            from germ_treatment as ns
            join germ_transfer as s
            on s.source_id = ns.id
            where s.target_id in (
                select x.id from germ_treatment as x
            )
            group by ns.id
        ) as cnts
        group by cnts.id
    ) as sub
    join (
        select
            nc.id,
            sum(c.germinated)::int as germinated
        from germ_treatment as nc
        join germ_count as c
        on c.treatment_id = nc.id
        group by nc.id
    ) as germ
    on sub.id = germ.id
);


-- germ_method --

drop function if exists germ_method;

create function germ_method (test int) 
returns table (path int[])
--returns table (id int)
language plpgsql as $$

    begin

    return query with recursive method as (
        select 
            x1.target_id as id,
            x1.target_id as source,
            array[x1.target_id] as path
        from germ_transfer as x1
        left join germ_transfer as x2
        on x1.target_id = x2.source_id
        where x2.source_id is null
        and x1.test_id = test
        union all
        select
            mi.id,
            x3.source_id as source,
            x3.source_id || mi.path
        from germ_transfer as x3
        join method as mi
        on mi.source = x3.target_id
    )
    select distinct on (m.id) 
        m.path
    from method as m
    order by m.id, cardinality(m.path) desc;
   
    end;
$$;


-- germ_status --

drop function if exists germ_status;

create function germ_status (
    test    int,
    day     int default 2147483647
) 
returns table (
    id          int,
    total       int,
    germinated  int,
    available   int
)
language plpgsql as $$

    begin

    return query with treatment as (
        select n.id
        from germ_treatment as n
        where n.test_id = test
        and n.start_day <= day
    )
    select
        sub.id,
        sub.total,
        germ.germinated,
        (sub.total - coalesce(germ.germinated, 0)) as available
    from (
        select
            cnts.id,
            sum(cnts.cnt)::int as total
        from (
            -- seeds moved into treatment from other treatments
            select
                nt.id,
                sum(t.seed_number) as cnt
            from treatment as nt
            join germ_transfer as t
            on t.target_id = nt.id
            group by nt.id 
            -- inventory seed sources  
            union select
                ni.id,
                sum(i.seed_number) as cnt
            from treatment as ni
            join germ_inventory as i
            on i.treatment_id = ni.id
            group by ni.id
            -- seeds sent on to other treatments
            union select
                ns.id,
                -sum(s.seed_number) as cnt
            from treatment as ns
            join germ_transfer as s
            on s.source_id = ns.id
            where s.target_id in (
                select x.id from treatment as x
            )
            group by ns.id
        ) as cnts
        group by cnts.id
    ) as sub
    left join (
        select
            nc.id,
            sum(c.germinated)::int as germinated
        from treatment as nc
        join germ_count as c
        on c.treatment_id = nc.id
        where c.count_day <= day
        group by nc.id
    ) as germ
    on sub.id = germ.id;
    
    end;
$$;