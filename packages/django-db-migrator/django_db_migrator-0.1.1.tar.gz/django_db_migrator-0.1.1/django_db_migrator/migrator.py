import subprocess
import logging
import os
from pathlib import Path
from dotenv import dotenv_values

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def read_env_file(env_path):
    logger.info(f"Reading environment variables from {env_path}")
    return dotenv_values(env_path)

def dump_database(env):
    db_name = env["DB_NAME"]
    db_user = env["DB_USER"]
    db_host = env["DB_HOST"]
    db_port = env.get("DB_PORT", "5432")
    output_file = f"{db_name}.dump"

    logger.info("Starting database dump...")
    try:
        subprocess.run(
            [
                "pg_dump",
                "-Fc",
                "-h", db_host,
                "-p", db_port,
                "-U", db_user,
                "-f", output_file,
                db_name
            ],
            check=True,
            env={**os.environ, "PGPASSWORD": env["DB_PASSWORD"]}
        )
        logger.info(f"Database dump completed: {output_file}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error dumping database: {e}")
        raise
    return output_file

def create_destination_db(dest_env):
    logger.info("Creating destination database and user if needed...")

    create_user_cmd = (
        f"psql -h {dest_env['DB_HOST']} -U {dest_env['DB_SUPERUSER']} -c "
        f"\"CREATE USER {dest_env['DB_USER']} WITH PASSWORD '{dest_env['DB_PASSWORD']}';\""
    )
    create_db_cmd = (
        f"psql -h {dest_env['DB_HOST']} -U {dest_env['DB_SUPERUSER']} -c "
        f"\"CREATE DATABASE {dest_env['DB_NAME']} OWNER {dest_env['DB_USER']};\""
    )

    try:
        subprocess.run(
            create_user_cmd,
            shell=True,
            check=True,
            env={**os.environ, "PGPASSWORD": dest_env["DB_SUPERUSER_PASSWORD"]}
        )
        logger.info("Destination user created (or already exists).")
    except subprocess.CalledProcessError:
        logger.warning("User may already exist. Skipping...")

    try:
        subprocess.run(
            create_db_cmd,
            shell=True,
            check=True,
            env={**os.environ, "PGPASSWORD": dest_env["DB_SUPERUSER_PASSWORD"]}
        )
        logger.info("Destination database created.")
    except subprocess.CalledProcessError:
        logger.warning("Database may already exist. Skipping...")

def restore_database(dump_file, dest_env):
    logger.info("Restoring dump into destination database...")
    try:
        subprocess.run(
            [
                "pg_restore",
                "-h", dest_env["DB_HOST"],
                "-p", dest_env.get("DB_PORT", "5432"),
                "-U", dest_env["DB_USER"],
                "-d", dest_env["DB_NAME"],
                "-c",
                dump_file
            ],
            check=True,
            env={**os.environ, "PGPASSWORD": dest_env["DB_PASSWORD"]}
        )
        logger.info("Database restored successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Restore failed: {e}")
        raise