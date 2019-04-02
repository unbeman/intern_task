create database shop;
\connect shop;

create table if not exists companies
(
	id serial not null
		constraint companies_pkey
			primary key,
	title varchar not null,
	description varchar
)
;

alter table companies owner to postgres
;

create table if not exists tags
(
	id serial not null
		constraint tags_pkey
			primary key,
	title varchar not null,
	constraint tags_title_id_key
		unique (title, id)
)
;

alter table tags owner to postgres
;

create table if not exists workers
(
	id serial not null
		constraint workers_pkey
			primary key,
	full_name varchar not null,
	position varchar not null,
	phone_number varchar not null,
	fk_company_id integer
		constraint workers_fk_company_id_fkey
			references companies
)
;

alter table workers owner to postgres
;

create table if not exists goods
(
	id serial not null
		constraint goods_pkey
			primary key,
	title varchar not null,
	description varchar,
	price integer not null,
	counts integer,
	fk_worker_id integer
		constraint goods_fk_worker_id_fkey
			references workers,
	fk_company_id integer
		constraint goods_fk_company_id_fkey
			references companies,
	constraint goods_title_fk_company_id_key
		unique (title, fk_company_id)
)
;

alter table goods owner to postgres
;

create table if not exists tags_to_goods
(
	tag_id integer not null
		constraint tags_to_goods_tag_id_fkey
			references tags,
	goods_id integer not null
		constraint tags_to_goods_goods_id_fkey
			references goods,
	constraint tags_to_goods_pkey
		primary key (tag_id, goods_id)
)
;

alter table tags_to_goods owner to postgres
;