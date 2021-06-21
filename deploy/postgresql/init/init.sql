create table if not exists "user"
(
    id           serial  not null
        constraint user_pkey
            primary key,
    first_name   varchar,
    last_name    varchar,
    email        varchar not null,
    password     varchar not null,
    is_active    boolean,
    is_superuser boolean
);

alter table "user"
    owner to postgres;

create index if not exists ix_user_id
    on "user" (id);

create unique index if not exists ix_user_email
    on "user" (email);

create index if not exists ix_user_last_name
    on "user" (last_name);

create index if not exists ix_user_first_name
    on "user" (first_name);


INSERT INTO public."user" (id, first_name, last_name, email, password, is_active, is_superuser) VALUES (1, 'ivan', 'greshnik', 'vlad@mail.com', '$pbkdf2-sha256$200000$X1AxbjVHQ2NweVlQcDF0Y2lwcU14cnYzbXFsUVNlZjlFWmRrYnBDVjVJbGlNVnByTEc1akxZWUNYaGszRVMxMVZveHBlRFRxWWx5ZTlnU08xQjdNaHc$iXyJOEgEtSrTaugvYtwqRycDgj7YTeVe9iLfFNGKVOA', true, true);
INSERT INTO public."user" (id, first_name, last_name, email, password, is_active, is_superuser) VALUES (2, 'Alar', 'Studios', 'alar@gmail.com', '$pbkdf2-sha256$200000$X1AxbjVHQ2NweVlQcDF0Y2lwcU14cnYzbXFsUVNlZjlFWmRrYnBDVjVJbGlNVnByTEc1akxZWUNYaGszRVMxMVZveHBlRFRxWWx5ZTlnU08xQjdNaHc$SBAkENaqr/auHwGuWbItJ7f498jnTpaOC3uqaRO.bko', true, true);
INSERT INTO public."user" (id, first_name, last_name, email, password, is_active, is_superuser) VALUES (3, 'vladislav', 'turic', 'vnep@gmail.com', '$pbkdf2-sha256$200000$X1AxbjVHQ2NweVlQcDF0Y2lwcU14cnYzbXFsUVNlZjlFWmRrYnBDVjVJbGlNVnByTEc1akxZWUNYaGszRVMxMVZveHBlRFRxWWx5ZTlnU08xQjdNaHc$SBAkENaqr/auHwGuWbItJ7f498jnTpaOC3uqaRO.bko', false, false);
INSERT INTO public."user" (id, first_name, last_name, email, password, is_active, is_superuser) VALUES (4, 'vladislav', 'nep', 'vladislavnep@gmail.com', '$pbkdf2-sha256$200000$X1AxbjVHQ2NweVlQcDF0Y2lwcU14cnYzbXFsUVNlZjlFWmRrYnBDVjVJbGlNVnByTEc1akxZWUNYaGszRVMxMVZveHBlRFRxWWx5ZTlnU08xQjdNaHc$SBAkENaqr/auHwGuWbItJ7f498jnTpaOC3uqaRO.bko', true, true);