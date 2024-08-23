-- -------------------------------------------------------------------
-- Создание пользователей и баз данных
-- -------------------------------------------------------------------

-- Создание пользователей для каждого проекта
CREATE USER prj1_user WITH ENCRYPTED PASSWORD 'prj1_pwd';
CREATE USER prj2_user WITH ENCRYPTED PASSWORD 'prj2_pwd';

-- Создание баз данных для каждого проекта с назначением владельцев
CREATE DATABASE prj1_db OWNER prj1_user;
CREATE DATABASE prj2_db OWNER prj2_user;

-- Подключение к базам данных и создание схем
\c prj1_db
CREATE SCHEMA prj1_schema AUTHORIZATION prj1_user;

\c prj2_db
CREATE SCHEMA prj2_schema AUTHORIZATION prj2_user;

-- Ограничение доступа к схемам
REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA prj1_schema FROM PUBLIC;
REVOKE ALL ON SCHEMA prj2_schema FROM PUBLIC;

GRANT USAGE ON SCHEMA prj1_schema TO prj1_user;
GRANT USAGE ON SCHEMA prj2_schema TO prj2_user;

-- Ограничение доступа к таблицам
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA prj1_schema FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA prj2_schema FROM PUBLIC;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA prj1_schema TO prj1_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA prj2_schema TO prj2_user;
