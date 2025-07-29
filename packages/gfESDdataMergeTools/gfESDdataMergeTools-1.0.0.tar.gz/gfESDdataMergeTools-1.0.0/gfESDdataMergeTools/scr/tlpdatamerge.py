import os
from xlrd import open_workbook
from PyQt5.QtWidgets import QApplication, QMessageBox
from collections import defaultdict
import platform
import traceback

class TLPDataMerge:
    """TLP data merging processing class"""
    def __init__(self, data_path, output_file, tester, log_callback=None):
        self.data_path = data_path
        self.output_file = f"{output_file}_TLP.txt"
        self.tester = tester
        self.total_files = 0
        self.processed_files = 0
        self.errors = []
        self.log_callback = log_callback
        self._app = None

    def process(self):
        if QApplication.instance() is None:
            self._app = QApplication([])
        
        try:
            self._log("=== Initialize TLP data processing ===")
            self._log(f"Root Directory: {self.data_path}")
            self._log(f"Output File: {self.output_file}")
            self._log(f"Tester selected: {self.tester}")

            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

            duplicates = self._check_device_names()
            if duplicates:
                self._show_duplicates_error(duplicates)
                return

            with open(self.output_file, 'w', encoding='utf-8') as output:
                xls_files = self._get_xls_files()
                self.total_files = len(xls_files)
                self._log(f"Found {self.total_files} Excel files")

                for idx, (file_path, rel_path) in enumerate(xls_files, 1):
                    self._log(f"Processing File ({idx}/{self.total_files}): {rel_path}")
                    self._process_single_file(file_path, rel_path, output)
                    self.processed_files += 1

            self._log("=== Data processing completed ===")
            message = f"Data merging completed! \nOutput File: {self.output_file}"

            if self.errors:
                self._log("\nErrors encountered during processing:")
                for error in self.errors:
                    self._log(f"- {error}")

            QMessageBox.information(
                None,
                "Processing completed", 
                message,
                QMessageBox.Ok
            )

        except Exception as e:
            error_msg = f"Fatal Error: {traceback.format_exc()}"
            self.errors.append(error_msg)
            self._log(error_msg)
            QMessageBox.critical(None, "Serious Error", str(e))

        finally:
            if platform.system() == "Windows":
                os.startfile(os.path.dirname(self.output_file))
            elif platform.system() == "Darwin":
                os.system(f"open '{os.path.dirname(self.output_file)}'")
            else:
                os.system(f"xdg-open '{os.path.dirname(self.output_file)}'")

    def _check_device_names(self):
        """Detect duplicate device names"""
        device_map = defaultdict(list)
        error_files = []
        xls_files = self._get_xls_files()

        self._log(f"Checking {len(xls_files)} duplicates of files...")

        for file_path, rel_path in xls_files:
            try:
                # Open the file using xlrd
                wb = open_workbook(file_path)
                
                # Get all worksheet names
                sheet_names = wb.sheet_names()
                
                if 'Parameters' not in sheet_names:
                    raise ValueError("Parameters worksheet is missing")
                
                params_ws = wb.sheet_by_name('Parameters')
                device_name = None
                
                # Traverse the parameter table (first 20 rows)
                for row_idx in range(min(20, params_ws.nrows)):
                    row = params_ws.row_values(row_idx)
                    if row[0] == 'Device Name/ID:':
                        device_name = row[1]
                        break
                
                if not device_name:
                    raise ValueError("Device name not found")
                
                device_map[device_name].append(rel_path)

            except Exception as e:
                error_msg = f"{rel_path} - {str(e)}"
                error_files.append(error_msg)
                self._log(f"{rel_path}Handling Errors: {traceback.format_exc()}")
                continue

        duplicates = {name: files for name, files in device_map.items() if len(files) > 1}
        if error_files:
            duplicates["[File Error]"] = error_files
            
        return duplicates

    def _show_duplicates_error(self, duplicates):
        """Show Duplicate Device Error Dialog"""
        error_msg = "The following problems were found: \n\n"
        
        if any(k != "[File Error]" for k in duplicates):
            error_msg += "Duplicate device name: \n"
            for name, files in duplicates.items():
                if name == "[File Error]":
                    continue
                error_msg += f"▸ {name} Exists in: \n"
                error_msg += "\n".join(f"   • {f}" for f in files) + "\n\n"
        
        if "[File Error]" in duplicates:
            error_msg += "\nFile Error: \n"
            error_msg += "\n".join(f"• {err}" for err in duplicates["[File Error]"])
        
        error_msg += "\n\nProcessing terminated"

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Data validation failed")
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(error_msg)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def _log(self, message):
        """Logging"""
        if self.log_callback:
            self.log_callback(message)
        print(message)

    def _get_xls_files(self):
        """Get all .xls files"""
        xls_files = []
        for root, dirs, files in os.walk(self.data_path):
            for file in files:
                if file.lower().endswith(('.xls', '.xlsx')):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.data_path)
                    xls_files.append((full_path, rel_path))
        return xls_files

    def _process_single_file(self, file_path, rel_path, output):
        """Processing a single file"""
        try:
            wb = open_workbook(file_path)
            
            # Write file header
            #header = [
            #    '=' * 40,
            #    f"Document source: {rel_path}",
            #    '=' * 40,
            #    ''
            #]
            #output.write('\n'.join(header) + '\n')
            #output.write('\n'.join(header))
            # Processing Parameters Table
            try:
                params_ws = wb.sheet_by_name('Parameters')
                # output.write("[Parameter]\n")
                for row_idx in range(params_ws.nrows):
                    row = params_ws.row_values(row_idx)
                    if row[0] or row[1]:
                        output.write(f"{row[0]}\t{row[1]}\n")
                #output.write("\n")
                output.write(f"Tester selected: {self.tester}\n")
            except:
                raise ValueError("Parameters worksheet is missing")

            # Processing Data Table
            try:
                data_ws = wb.sheet_by_name('Data')
                headers = data_ws.row_values(0)
                
                # Determine the leaking column name
                leakage_col = "I(LEAKAGE)" if "Leakage (A)" in headers else "V(LEAKAGE)"
                
                # Write data header
                #output.write("[Data]\n")
                output.write("TLP I(AMPS)\tTLP V(VOLTS)\t{}\n".format(leakage_col))
                
                # Extract columns B(1), C(2), D(3) (xlrd starts counting from 0)
                for row_idx in range(1, data_ws.nrows):
                    row = data_ws.row_values(row_idx)
                    # Extract columns 2, 3, and 4 (index 1, 2, 3)
                    output_line = "\t".join([
                        str(row[2]),  # Column C
                        str(row[1]),  # Column B
                        str(row[3])   # Column D
                    ]) + "\n"
                    output.write(output_line)
                
                # output.write("\n")
            except:
                raise ValueError("Missing Data worksheet")

        except Exception as e:
            error_msg = f"Process {rel_path} error:\n{traceback.format_exc()}"
            self.errors.append(error_msg)
            self._log(error_msg)

if __name__ == "__main__":
    app = QApplication([])
    
    merger = TLPDataMerge(
        data_path=r"E:\Your\Input\Path",
        output_file=r"E:\Your\Output\Path\Merged"
    )
    
    def log_callback(msg):
        print(f"[Log] {msg}")
    
    merger.log_callback = log_callback
    merger.process()
    
    app.exec_()