import argparse
from .migrator import read_env_file, dump_database, restore_database, create_destination_db

def main():
    parser = argparse.ArgumentParser(description="Migrate a Django PostgreSQL database to a new host.")
    parser.add_argument("--source-env", type=str, required=True, help="Path to source .env file")
    parser.add_argument("--dest-env", type=str, required=True, help="Path to destination .env file")

    args = parser.parse_args()

    source_env = read_env_file(args.source_env)
    dest_env = read_env_file(args.dest_env)

    dump_file = dump_database(source_env)
    create_destination_db(dest_env)
    restore_database(dump_file, dest_env)

if __name__ == "__main__":
    main()