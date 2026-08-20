import sys
import app.crud_storage as storage
import app.crud_database as db

def display_menu():
    print("\n--- Supabase File CRUD Menu ---")
    print("1. Upload File (Create in Storage + DB + Trigger Edge Function)")
    print("2. List Files (Read from Storage and DB)")
    print("3. Download File (Read from Storage)")
    print("4. Update/Replace File (Update in Storage)")
    print("5. Delete File (Delete from Storage + DB)")
    print("6. Update DB Record Name (Update in DB only)")
    print("0. Exit")
    print("-------------------------------")

def main():
    while True:
        display_menu()
        choice = input("Enter choice: ").strip()

        if choice == '1':
            path = input("Enter local file path to upload: ").strip()
            storage.upload_file(path)
        
        elif choice == '2':
            print("\n--- Storage Buckets ---")
            storage.list_files()
            print("\n--- Database Table ---")
            db.list_file_metadata()

        elif choice == '3':
            name = input("Enter file name in storage: ").strip()
            dest = input("Enter local destination path: ").strip()
            storage.download_file(name, dest)

        elif choice == '4':
            name = input("Enter file name in storage to replace: ").strip()
            path = input("Enter local file path to upload as replacement: ").strip()
            storage.update_file(name, path)

        elif choice == '5':
            name = input("Enter file name to delete: ").strip()
            storage.delete_file(name)
            db.delete_file_metadata(name)

        elif choice == '6':
            rec_id = input("Enter DB Record ID to update: ").strip()
            new_name = input("Enter new filename: ").strip()
            db.update_file_metadata(rec_id, new_name)

        elif choice == '0':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    try:
        # Test if env is set properly before starting
        from app.config import SUPABASE_URL, SUPABASE_KEY
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("WARNING: SUPABASE_URL or SUPABASE_KEY not found in .env")
            print("Please configure them before using the app.")
        
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
