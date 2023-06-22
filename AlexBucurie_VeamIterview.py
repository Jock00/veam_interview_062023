import os
import sys
import shutil
import hashlib
import time


class FolderSynchronizer:
    def __init__(self, source_folder, replica_folder, sync_interval, log_file):
        self.source_folder = source_folder
        self.replica_folder = replica_folder
        self.sync_interval = sync_interval
        self.log_file = log_file

    def synchronize(self):
        print("Starting folder synchronization...")
        self.log("Starting folder synchronization...")

        while True:
            start_time = time.time()

            self.log("\nSyncing folders at: {}".format(time.ctime()))

            self.sync_files()

            elapsed_time = time.time() - start_time
            remaining_time = self.sync_interval - elapsed_time

            if remaining_time > 0:
                time.sleep(remaining_time)

    def sync_files(self):
        source_files = self.get_files_in_folder(self.source_folder)
        replica_files = self.get_files_in_folder(self.replica_folder)

        self.delete_extra_files(replica_files, source_files)
        self.copy_missing_files(source_files, replica_files)

    def get_files_in_folder(self, folder):
        file_list = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder)
                file_list.append(relative_path)
        return file_list

    def delete_extra_files(self, replica_files, source_files):
        for file in replica_files:
            if file not in source_files:
                file_path = os.path.join(self.replica_folder, file)
                os.remove(file_path)
                self.log("Deleted file: {}".format(file_path))

    def copy_missing_files(self, source_files, replica_files):
        for file in source_files:
            if file not in replica_files:
                source_path = os.path.join(self.source_folder, file)
                replica_path = os.path.join(self.replica_folder, file)
                os.makedirs(os.path.dirname(replica_path), exist_ok=True)
                shutil.copy2(source_path, replica_path)
                self.log("Copied file: {}".format(replica_path))

    def log(self, message):
        with open(self.log_file, 'a') as f:
            f.write(message + '\n')
        print(message)


def calculate_md5(file_path):
    with open(file_path, 'rb') as f:
        md5_hash = hashlib.md5()
        while True:
            data = f.read(4096)
            if not data:
                break
            md5_hash.update(data)
    return md5_hash.hexdigest()


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python folder_synchronizer.py <source_folder> <replica_folder> <sync_interval> <log_file>")
        sys.exit(1)

    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    sync_interval = int(sys.argv[3])
    log_file = sys.argv[4]

    synchronizer = FolderSynchronizer(source_folder, replica_folder, sync_interval, log_file)
    synchronizer.synchronize()
