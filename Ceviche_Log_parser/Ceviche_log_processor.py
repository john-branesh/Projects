import re
import os

class LogProcessor:
    def __init__(self, logs_dir, initial_keywords, additional_keywords, file_encoding, output_dir):
        self.logs_dir = logs_dir
        self.initial_keywords = initial_keywords
        self.additional_keywords = additional_keywords
        self.file_encoding = file_encoding
        self.output_dir = output_dir

        # Compile regex patterns once
        self.initial_patterns = {kw: re.compile(kw) for kw in initial_keywords}
        self.additional_patterns = {kw: re.compile(kw) for kw in additional_keywords}

        # Create the output directory if it doesn't exist
        self.create_output_directory()

    # Creating Output Folder
    def create_output_directory(self):
        os.makedirs(self.output_dir, exist_ok=True)

    def process_logs(self):
        # Iterate over each initial keyword
        for initial_keyword in self.initial_keywords:
            # Create a folder for the current initial keyword
            initial_folder_path = os.path.join(self.output_dir, initial_keyword)
            os.makedirs(initial_folder_path, exist_ok=True)

            # Create an output file handle for the current initial keyword
            output_file_path = os.path.join(initial_folder_path, f"{initial_keyword}_output.txt")
            with open(output_file_path, "w", encoding=self.file_encoding) as output_file:
                # Get a list of all log files in the "LOGS" directory
                log_file_paths = [os.path.join(self.logs_dir, filename) for filename in os.listdir(self.logs_dir) if filename.endswith(".txt")]

                # Process each log file
                for log_file_path in log_file_paths:
                    with open(log_file_path, "r", encoding=self.file_encoding, errors="replace") as log_file:
                        for line in log_file:
                            if re.search(initial_keyword, line):
                                output_file.write(line.strip() + "\n")

        print("Initial output files created in the 'output_files' directory.")

    def search_additional_keywords(self):
        # Iterate over each initial keyword
        for initial_keyword in self.initial_keywords:
            # Create a folder for the current initial keyword
            initial_folder_path = os.path.join(self.output_dir, initial_keyword)

            # Iterate over each additional keyword for the current initial keyword
            for additional_keyword in self.additional_keywords:
                # Create an output file handle for the current additional keyword
                additional_output_file_path = os.path.join(initial_folder_path, f"{initial_keyword}_{additional_keyword}_output.txt")
                with open(additional_output_file_path, "w", encoding=self.file_encoding) as additional_output_file:
                    # Process the output file corresponding to the current initial keyword
                    initial_output_file_path = os.path.join(initial_folder_path, f"{initial_keyword}_output.txt")

                    # Check if the initial output file exists before attempting to open it
                    if os.path.isfile(initial_output_file_path):
                        with open(initial_output_file_path, "r", encoding=self.file_encoding,
                                  errors="replace") as initial_output_file:
                            for line in initial_output_file:
                                if re.search(additional_keyword, line):
                                    additional_output_file.write(line.strip() + "\n")
                    else:
                        print(f"File not found: {initial_output_file_path}")

        print("Additional output files created in the 'output_files' directory.")

if __name__ == "__main__":
    # Add your additional keywords here
    initial_keywords = ["Enter your Parent keywords"]
    additional_keywords = ["Enter your child keywords"]
    # Directory containing log files
    logs_dir = "LOGS"
    # Replace with the correct encoding if known
    file_encoding = "utf-8"
    # Directory to store the output files
    output_dir = "output_files"

    log_processor = LogProcessor(logs_dir, initial_keywords, additional_keywords, file_encoding, output_dir)
    log_processor.process_logs()
    log_processor.search_additional_keywords()
