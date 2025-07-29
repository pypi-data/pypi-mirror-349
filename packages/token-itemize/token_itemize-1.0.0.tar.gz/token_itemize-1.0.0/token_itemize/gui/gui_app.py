# token_itemize/gui/gui_app.py
import os
import sys
import csv
import json
from importlib.resources import files as pkg_files
import base64

# Unset the QT_QPA_PLATFORM_PLUGIN_PATH variable to avoid conflicts from cv2's Qt plugins.
if "QT_QPA_PLATFORM_PLUGIN_PATH" in os.environ:
    del os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"]

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QCheckBox,
    QProgressBar,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QListWidget,
    QGroupBox,
    QScrollArea,
    QComboBox,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap

from token_itemize.tokenizers import text_tokenizer, image_tokenizer, audio_tokenizer, video_tokenizer
from token_itemize.api.api_client import get_api_client
from token_itemize.config import load_config
from token_itemize.utils import get_cached_token_count, set_cached_token_count
from token_itemize.styles import StyleHelper

class TokenizeWorker(QThread):
    resultReady = pyqtSignal(dict)
    progressUpdate = pyqtSignal(int)
    errorOccurred = pyqtSignal(str)

    def __init__(self, files, prompt, api_mode, endpoint, model, api_key, provider, verbose, cost_rate, save_transcript):
        super().__init__()
        self.files = files
        self.prompt = prompt
        self.api_mode = api_mode
        self.endpoint = endpoint
        self.model = model
        self.api_key = api_key
        self.provider = provider
        self.verbose = verbose
        self.cost_rate = cost_rate
        self.save_transcript = save_transcript

    def run(self):
        try:
            if self.api_mode:
                client = get_api_client(
                    provider=self.provider,
                    endpoint=self.endpoint,
                    model=self.model,
                    api_key=self.api_key,
                    cost_rate=self.cost_rate,
                    verbose=self.verbose
                )
                self.progressUpdate.emit(50)
                result = client.count_tokens(files=self.files, prompt=self.prompt)
                self.progressUpdate.emit(100)
                self.resultReady.emit(result)
            else:
                # Local token counting
                total_items = len(self.files) + (1 if self.prompt else 0)
                processed_items = 0
                results = []
                total_input_tokens = 0
                for file in self.files:
                    try:
                        tokens, details = self.process_file(file)
                        results.append({
                            "file": file,
                            "tokens": tokens,
                            "details": details
                        })
                        if isinstance(tokens, (int, float)):
                            total_input_tokens += tokens
                    except Exception as e:
                        results.append({
                            "file": file,
                            "tokens": "Error",
                            "details": str(e)
                        })
                    processed_items += 1
                    self.progressUpdate.emit(int((processed_items / total_items) * 100))

                if self.prompt:
                    tokens, details = text_tokenizer.count_text_tokens(self.prompt, verbose=self.verbose)
                    results.append({
                        "prompt": self.prompt,
                        "tokens": tokens,
                        "details": details
                    })
                    total_input_tokens += tokens
                    processed_items += 1
                    self.progressUpdate.emit(int((processed_items / total_items) * 100))

                cost = (total_input_tokens / 1000) * self.cost_rate
                output_data = {
                    "results": results,
                    "total_tokens": total_input_tokens,
                    "total_cost": cost
                }
                self.resultReady.emit(output_data)
        except Exception as e:
            self.errorOccurred.emit(str(e))

    def process_file(self, file_path):
        cached = get_cached_token_count(file_path)
        if cached is not None:
            if self.verbose:
                print(f"Cache hit for {file_path}: {cached} tokens")
            return int(cached), "Cached result"

        ext = os.path.splitext(file_path)[1].lower()
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif']
        audio_extensions = ['.wav', '.mp3', '.flac', '.aac', '.ogg']
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
        if ext in image_extensions:
            tokens, details = image_tokenizer.count_image_tokens(file_path, verbose=self.verbose)
        elif ext in audio_extensions:
            tokens, details = audio_tokenizer.count_audio_tokens(file_path, verbose=self.verbose)
        elif ext in video_extensions:
            tokens, details = video_tokenizer.count_video_tokens(file_path, verbose=self.verbose)
        else:
            # Default to text tokenizer for all other extensions
            tokens, details = text_tokenizer.count_text_file_tokens(file_path, verbose=self.verbose)

        set_cached_token_count(file_path, tokens)
        return tokens, details

class TokenItemizeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.current_theme = self.config.get('dark_mode', False)
        self.files = []
        self.thread = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Token Itemize")
        # Reduce from 1024x768 to 900x600 to help ensure bottom is visible
        self.setMinimumSize(900, 600)

        # Apply theme if in dark mode
        app = QApplication.instance()
        if app:
            StyleHelper.apply_theme(app, dark_mode=self.current_theme)

        # Main scrollable area
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        mainWidget = QWidget()
        scrollArea.setWidget(mainWidget)
        mainLayout = QVBoxLayout(mainWidget)
        mainLayout.setContentsMargins(16, 16, 16, 16)
        mainLayout.setSpacing(16)

        # --- Header: Logo & Theme Toggle ---
        header_layout = QHBoxLayout()
        logo_label = QLabel()
        try:
            logo_path = str(pkg_files("token_itemize.assets").joinpath("logo.png"))
        except Exception:
            logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/logo.png"))
        if not os.path.exists(logo_path):
            logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../assets/logo.png"))
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(logo_label)

        header_layout.addStretch(1)
        self.theme_toggle = QPushButton("☀️" if self.current_theme else "🌙")
        self.theme_toggle.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_toggle)
        mainLayout.addLayout(header_layout)

        # --- Files / Folders Group ---
        file_group = QGroupBox("Files / Folders")
        file_layout = QVBoxLayout()
        file_group.setLayout(file_layout)
        self.fileListWidget = QListWidget()
        file_layout.addWidget(self.fileListWidget)
        file_buttons_layout = QHBoxLayout()
        self.add_files_btn = QPushButton("Add Files")
        self.add_files_btn.clicked.connect(self.addFiles)
        file_buttons_layout.addWidget(self.add_files_btn)
        self.add_folder_btn = QPushButton("Add Folder")
        self.add_folder_btn.clicked.connect(self.addFolder)
        file_buttons_layout.addWidget(self.add_folder_btn)
        self.clear_btn = QPushButton("Clear Selection")
        self.clear_btn.clicked.connect(self.clearFiles)
        file_buttons_layout.addWidget(self.clear_btn)
        file_layout.addLayout(file_buttons_layout)
        mainLayout.addWidget(file_group)

        # --- Gitignore Checkbox ---
        self.gitignoreCheckBox = QCheckBox("Apply .gitignore filtering")
        mainLayout.addWidget(self.gitignoreCheckBox)

        # --- Prompt Group ---
        prompt_group = QGroupBox("Prompt")
        prompt_layout = QHBoxLayout()
        prompt_group.setLayout(prompt_layout)
        prompt_layout.addWidget(QLabel("Prompt:"))
        self.promptLineEdit = QLineEdit()
        prompt_layout.addWidget(self.promptLineEdit)
        mainLayout.addWidget(prompt_group)

        # --- API Options Group ---
        api_group = QGroupBox("API Options")
        api_layout = QVBoxLayout()
        api_group.setLayout(api_layout)
        self.apiCheckBox = QCheckBox("Enable API Mode")
        self.apiCheckBox.stateChanged.connect(self.toggleApiOptions)
        api_layout.addWidget(self.apiCheckBox)
        api_layout.addWidget(QLabel("Endpoint:"))
        self.endpointLineEdit = QLineEdit()
        self.endpointLineEdit.setPlaceholderText("Endpoint")
        api_layout.addWidget(self.endpointLineEdit)
        api_layout.addWidget(QLabel("Model:"))
        self.modelLineEdit = QLineEdit()
        self.modelLineEdit.setPlaceholderText("Model")
        api_layout.addWidget(self.modelLineEdit)
        api_layout.addWidget(QLabel("API Key:"))
        self.apiKeyLineEdit = QLineEdit()
        self.apiKeyLineEdit.setPlaceholderText("API Key")
        self.apiKeyLineEdit.setEchoMode(QLineEdit.Password)
        api_layout.addWidget(self.apiKeyLineEdit)

        provider_layout = QHBoxLayout()
        provider_label = QLabel("Provider:")
        provider_layout.addWidget(provider_label)
        self.providerComboBox = QComboBox()
        self.providerComboBox.addItems(["ollama", "openai", "deepseek", "openrouter"])
        provider_layout.addWidget(self.providerComboBox)
        api_layout.addLayout(provider_layout)

        self.saveTranscriptCheckBox = QCheckBox("Save Conversation Transcript")
        api_layout.addWidget(self.saveTranscriptCheckBox)
        self.verboseCheckBox = QCheckBox("Verbose Logging")
        api_layout.addWidget(self.verboseCheckBox)
        mainLayout.addWidget(api_group)

        # --- Control Buttons: Count Tokens + Export Results side-by-side ---
        controls_layout = QHBoxLayout()
        self.countButton = QPushButton("Count Tokens")
        self.countButton.clicked.connect(self.startCounting)
        controls_layout.addWidget(self.countButton)
        self.exportButton = QPushButton("Export Results")
        self.exportButton.clicked.connect(self.exportResults)
        controls_layout.addWidget(self.exportButton)
        mainLayout.addLayout(controls_layout)

        # --- Progress Bar ---
        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        mainLayout.addWidget(self.progressBar)

        # --- Results Table ---
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()
        results_group.setLayout(results_layout)
        self.resultsTable = QTableWidget()
        self.resultsTable.setColumnCount(3)
        self.resultsTable.setHorizontalHeaderLabels(["File/Prompt", "Tokens", "Details"])
        self.resultsTable.horizontalHeader().setStretchLastSection(True)
        # Remove minimum height so it can shrink if needed
        results_layout.addWidget(self.resultsTable)
        mainLayout.addWidget(results_group)

        self.setCentralWidget(scrollArea)
        self.toggleApiOptions()

    def toggle_theme(self):
        self.current_theme = not self.current_theme
        app = QApplication.instance()
        if app:
            StyleHelper.apply_theme(app, dark_mode=self.current_theme)
        self.theme_toggle.setText("☀️" if self.current_theme else "🌙")
        self.save_config()

    def save_config(self):
        try:
            from token_itemize.config import load_config
            import yaml
            config = load_config()
            config['dark_mode'] = self.current_theme
            with open("config.yaml", "w") as f:
                yaml.dump(config, f)
        except Exception as e:
            print(f"Error saving config: {e}")

    def addFiles(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if files:
            for file in files:
                if file not in self.files:
                    self.files.append(file)
                    self.fileListWidget.addItem(file)

    def addFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            for root, _, filenames in os.walk(folder):
                for filename in filenames:
                    full_path = os.path.join(root, filename)
                    if full_path not in self.files:
                        self.files.append(full_path)
                        self.fileListWidget.addItem(full_path)

    def clearFiles(self):
        self.files = []
        self.fileListWidget.clear()

    def toggleApiOptions(self):
        api_enabled = self.apiCheckBox.isChecked()
        self.endpointLineEdit.setEnabled(api_enabled)
        self.modelLineEdit.setEnabled(api_enabled)
        self.apiKeyLineEdit.setEnabled(api_enabled)
        self.providerComboBox.setEnabled(api_enabled)
        self.saveTranscriptCheckBox.setEnabled(api_enabled)
        self.verboseCheckBox.setEnabled(api_enabled)

    def startCounting(self):
        self.countButton.setEnabled(False)
        self.progressBar.setValue(0)
        prompt = self.promptLineEdit.text().strip()
        api_mode = self.apiCheckBox.isChecked()
        endpoint = self.endpointLineEdit.text().strip()
        model = self.modelLineEdit.text().strip()
        api_key = self.apiKeyLineEdit.text().strip()
        provider = self.providerComboBox.currentText()
        verbose = self.verboseCheckBox.isChecked()
        cost_rate = 0.03
        save_transcript = self.saveTranscriptCheckBox.isChecked()

        file_list = self.files
        if self.gitignoreCheckBox.isChecked():
            file_list = self.filter_files_by_gitignore(file_list)

        self.worker = TokenizeWorker(
            files=file_list,
            prompt=prompt,
            api_mode=api_mode,
            endpoint=endpoint,
            model=model,
            api_key=api_key,
            provider=provider,
            verbose=verbose,
            cost_rate=cost_rate,
            save_transcript=save_transcript
        )
        self.worker.progressUpdate.connect(self.updateProgress)
        self.worker.resultReady.connect(self.displayResults)
        self.worker.errorOccurred.connect(self.handleError)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(lambda: self.worker.run())
        self.thread.start()

    def filter_files_by_gitignore(self, files):
        try:
            import pathspec
            gitignore_path = os.path.join(os.getcwd(), ".gitignore")
            if os.path.exists(gitignore_path):
                with open(gitignore_path, "r") as f:
                    lines = f.read().splitlines()
                spec = pathspec.PathSpec.from_lines("gitwildmatch", lines)
                filtered_files = [f for f in files if not spec.match_file(os.path.relpath(f, os.getcwd()))]
                return filtered_files
            else:
                QMessageBox.warning(self, "Gitignore Filter", ".gitignore file not found in the current directory.")
                return files
        except Exception as e:
            QMessageBox.warning(self, "Gitignore Filter Error", f"Error applying .gitignore filtering: {e}")
            return files

    def updateProgress(self, value):
        self.progressBar.setValue(value)

    def displayResults(self, result):
        self.resultsTable.setRowCount(0)
        if "results" in result:
            for item in result["results"]:
                row = self.resultsTable.rowCount()
                self.resultsTable.insertRow(row)
                file_prompt = item.get("file", item.get("prompt", ""))
                self.resultsTable.setItem(row, 0, QTableWidgetItem(str(file_prompt)))
                self.resultsTable.setItem(row, 1, QTableWidgetItem(str(item.get("tokens", ""))))
                self.resultsTable.setItem(row, 2, QTableWidgetItem(str(item.get("details", ""))))
        row = self.resultsTable.rowCount()
        self.resultsTable.insertRow(row)
        self.resultsTable.setItem(row, 0, QTableWidgetItem("Total"))
        self.resultsTable.setItem(row, 1, QTableWidgetItem(str(result.get("total_tokens", ""))))
        total_cost_str = f"Cost: ${result.get('total_cost', 0):.4f}"
        self.resultsTable.setItem(row, 2, QTableWidgetItem(total_cost_str))
        self.countButton.setEnabled(True)
        if self.worker.save_transcript:
            try:
                conversation = {
                    "provider": self.providerComboBox.currentText(),
                    "prompt": self.promptLineEdit.text().strip(),
                    "files": self.files,
                    "response": result.get("full_response", ""),
                    "input_tokens": result.get("input_tokens", 0),
                    "output_tokens": result.get("output_tokens", 0)
                }
                from token_itemize.api.conversation_saver import save_conversation_markdown
                transcript_file = save_conversation_markdown(conversation)
                QMessageBox.information(self, "Transcript Saved", f"Conversation transcript saved to {transcript_file}")
            except Exception as e:
                QMessageBox.warning(self, "Transcript Save Error", f"Failed to save transcript: {e}")
        self.thread.quit()

    def handleError(self, message):
        QMessageBox.critical(self, "Error", message)
        self.countButton.setEnabled(True)
        self.thread.quit()

    def exportResults(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Export Results", "", "CSV Files (*.csv);;JSON Files (*.json)", options=options
        )
        if fileName:
            try:
                rowCount = self.resultsTable.rowCount()
                colCount = self.resultsTable.columnCount()
                headers = [self.resultsTable.horizontalHeaderItem(i).text() for i in range(colCount)]
                data = []
                for row in range(rowCount):
                    row_data = []
                    for col in range(colCount):
                        item = self.resultsTable.item(row, col)
                        row_data.append(item.text() if item else "")
                    data.append(row_data)
                if fileName.endswith(".csv"):
                    with open(fileName, "w", newline="") as csvfile:
                        import csv
                        writer = csv.writer(csvfile)
                        writer.writerow(headers)
                        writer.writerows(data)
                elif fileName.endswith(".json"):
                    with open(fileName, "w") as jsonfile:
                        json.dump({"results": data}, jsonfile, indent=2)
                QMessageBox.information(self, "Export", f"Results exported to {fileName}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", str(e))

def launch_gui():
    app = QApplication(sys.argv)
    gui = TokenItemizeGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    launch_gui()
