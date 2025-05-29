class FileProcessor {
  constructor() {
    this.selectedFiles = new Set();
    this.fileTreeData = [];
    this.expandedFolders = new Set();
    this.upload_id = null;
    this.pathTypeMap = new Map();
    this.init();
  }

  init() {
    this.setupFileUploads();
    this.setupFormSubmission();
    this.setupPopupEvents();
  }

  setupFileUploads() {
    const docxFile = document.getElementById('docxFile');
    const docxDropZone = document.getElementById('docxDropZone');
    const docxFileName = document.getElementById('docxFileName');

    docxDropZone.addEventListener('click', () => docxFile.click());
    docxFile.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        docxFileName.textContent = `Selected: ${file.name}`;
        docxFileName.classList.remove('hidden');
      }
    });

    const zipFile = document.getElementById('zipFile');
    const zipDropZone = document.getElementById('zipDropZone');
    const zipFileName = document.getElementById('zipFileName');

    zipDropZone.addEventListener('click', () => zipFile.click());
    zipFile.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        zipFileName.textContent = `Selected: ${file.name}`;
        zipFileName.classList.remove('hidden');
      }
    });

    [docxDropZone, zipDropZone].forEach(zone => {
      zone.addEventListener('dragover', (e) => {
        e.preventDefault();
        zone.classList.add('border-blue-400', 'bg-blue-50');
      });

      zone.addEventListener('dragleave', () => {
        zone.classList.remove('border-blue-400', 'bg-blue-50');
      });

      zone.addEventListener('drop', (e) => {
        e.preventDefault();
        zone.classList.remove('border-blue-400', 'bg-blue-50');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
          const targetInput = zone.id === 'docxDropZone' ? docxFile : zipFile;
          targetInput.files = files;
          targetInput.dispatchEvent(new Event('change'));
        }
      });
    });
  }

  setupFormSubmission() {
    const form = document.getElementById('uploadForm');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      await this.handleFormSubmit();
    });
  }

  setupPopupEvents() {
    const popup = document.getElementById('popup');
    const closePopup = document.getElementById('closePopup');
    const cancelPopup = document.getElementById('cancelPopup');
    const submitPopup = document.getElementById('submitPopup');

    closePopup.addEventListener('click', () => this.hidePopup());
    cancelPopup.addEventListener('click', () => this.hidePopup());
    submitPopup.addEventListener('click', () => this.handlePopupSubmit());

    popup.addEventListener('click', (e) => {
      if (e.target === popup) {
        this.hidePopup();
      }
    });
  }

  async handleFormSubmit() {
    const docxFile = document.getElementById('docxFile').files[0];
    const zipFile = document.getElementById('zipFile').files[0];
    if (!docxFile || !zipFile) {
      alert('Please select both DOCX template and ZIP file');
      return;
    }
    this.showLoading(true);

    try {
      const formData = new FormData();
      formData.append('docx_template', docxFile);
      formData.append('zip_file', zipFile);

      const response = await fetch('/api/upload-files', { method: 'POST', body: formData });
      if (!response.ok) throw new Error('Upload failed');

      const data = await response.json();
      this.fileTreeData = data.files;
      this.upload_id = data.upload_id;

      this._buildPathTypeMap(this.fileTreeData);

      this.selectedFiles.clear();
      this.initializeSelectedFiles(data.files);

      this.showPopup();
      this.renderFileTree();

    } catch (err) {
      console.error(err);
      alert('Error uploading files. Please try again.');
    } finally {
      this.showLoading(false);
    }
  }

  _buildPathTypeMap(files, parentPath = '') {
    for (const file of files) {
      const fullPath = parentPath ? `${parentPath}/${file.name}` : file.name;
      this.pathTypeMap.set(fullPath, file.type);
      if (file.type === 'directory' && file.children) {
        this._buildPathTypeMap(file.children, fullPath);
      }
    }
  }

  initializeSelectedFiles(files, path = '') {
    files.forEach(file => {
      const fullPath = path ? `${path}/${file.name}` : file.name;

      if (file.type === 'directory') {
        this.selectedFiles.add(fullPath);
        this.expandedFolders.add(fullPath);
        if (file.children) {
          this.initializeSelectedFiles(file.children, fullPath);
        }
      } else {
        this.selectedFiles.add(fullPath);
      }
    });
  }

  showPopup() {
    document.getElementById('popup').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }

  hidePopup() {
    document.getElementById('popup').classList.add('hidden');
    document.body.style.overflow = 'auto';
  }

  renderFileTree() {
    const treeContainer = document.getElementById('fileTree');
    treeContainer.innerHTML = this.generateTreeHTML(this.fileTreeData);

    treeContainer.addEventListener('change', (e) => {
      if (e.target.type === 'checkbox') {
        this.handleFileSelection(e.target);
      }
    });

    treeContainer.addEventListener('click', (e) => {
      if (e.target.classList.contains('folder-toggle') || e.target.closest('.folder-toggle')) {
        const button = e.target.classList.contains('folder-toggle') ? e.target : e.target.closest('.folder-toggle');
        this.toggleFolder(button);
      }
    });
  }

  generateTreeHTML(files, level = 0, path = '') {
    let html = '';

    files.forEach((file, index) => {
      const fullPath = path ? `${path}/${file.name}` : file.name;
      const isSelected = this.selectedFiles.has(fullPath);
      const indent = '  '.repeat(level);

      if (file.type === 'directory') {
        const hasChildren = file.children && file.children.length > 0;
        const folderId = `folder-${fullPath.replace(/[^a-zA-Z0-9]/g, '_')}`;
        const isExpanded = this.expandedFolders.has(fullPath);

        html += `<div class="mb-1">
                    <div class="flex items-center space-x-2 py-1 hover:bg-gray-100 rounded px-1">
                        <span class="text-gray-400 whitespace-pre">${indent}</span>
                        ${hasChildren ?
            `<button class="folder-toggle w-4 h-4 flex items-center justify-center text-gray-500 hover:text-gray-700" data-folder-path="${fullPath}">
                                <svg class="w-3 h-3 transform transition-transform ${isExpanded ? 'rotate-90' : ''}" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                                </svg>
                            </button>` :
            '<span class="w-4"></span>'
          }
                        <input type="checkbox" ${isSelected ? 'checked' : ''}
                               data-path="${fullPath}" data-type="${file.type}"
                               class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                        <span class="text-sm flex items-center">
                            <span class="mr-2">📁</span>
                            <span class="font-medium text-blue-700">${file.name}</span>
                        </span>
                    </div>`;

        if (hasChildren) {
          html += `<div id="${folderId}" class="folder-content" style="display: ${isExpanded ? 'block' : 'none'}">
                        ${this.generateTreeHTML(file.children, level + 1, fullPath)}
                    </div>`;
        }

        html += '</div>';
      } else {
        // File
        const fileExtension = file.name.split('.').pop().toLowerCase();
        const fileIcon = this.getFileIcon(fileExtension);

        html += `<div class="flex items-center space-x-2 py-1 hover:bg-gray-100 rounded px-1">
                    <span class="text-gray-400 whitespace-pre">${indent}</span>
                    <span class="w-4"></span>
                    <input type="checkbox" ${isSelected ? 'checked' : ''}
                           data-path="${fullPath}" data-type="${file.type}"
                           class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                    <span class="text-sm flex items-center">
                        <span class="mr-2">${fileIcon}</span>
                        <span class="text-gray-800">${file.name}</span>
                    </span>
                </div>`;
      }
    });

    return html;
  }

  getFileIcon(extension) {
    const iconMap = {
      'js': '🟨',
      'ts': '🔷',
      'html': '🌐',
      'css': '🎨',
      'json': '📋',
      'md': '📝',
      'txt': '📄',
      'py': '🐍',
      'java': '☕',
      'cpp': '⚙️',
      'c': '⚙️',
      'php': '🐘',
      'rb': '💎',
      'go': '🐹',
      'rs': '🦀',
      'xml': '📰',
      'yml': '⚙️',
      'yaml': '⚙️',
      'png': '🖼️',
      'jpg': '🖼️',
      'jpeg': '🖼️',
      'gif': '🖼️',
      'svg': '🎭',
      'pdf': '📕',
      'zip': '📦',
      'tar': '📦',
      'gz': '📦'
    };

    return iconMap[extension] || '📄';
  }

  toggleFolder(button) {
    const folderPath = button.dataset.folderPath;
    const folderId = `folder-${folderPath.replace(/[^a-zA-Z0-9]/g, '_')}`;
    const folderContent = document.getElementById(folderId);
    const arrow = button.querySelector('svg');

    if (this.expandedFolders.has(folderPath)) {
      // Collapse folder
      this.expandedFolders.delete(folderPath);
      folderContent.style.display = 'none';
      arrow.classList.remove('rotate-90');
    } else {
      this.expandedFolders.add(folderPath);
      folderContent.style.display = 'block';
      arrow.classList.add('rotate-90');
    }
  }

  handleFileSelection(checkbox) {
    const path = checkbox.dataset.path;
    const type = checkbox.dataset.type;

    if (checkbox.checked) {
      this.selectedFiles.add(path);

      if (type === 'directory') {
        this.selectAllChildren(path);
      }
    } else {
      this.selectedFiles.delete(path);

      if (type === 'directory') {
        this.deselectAllChildren(path);
      }
    }

    this.updateCheckboxStates();
  }

  updateCheckboxStates() {
    const checkboxes = document.querySelectorAll('#fileTree input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
      const path = checkbox.dataset.path;
      checkbox.checked = this.selectedFiles.has(path);
    });
  }

  selectAllChildren(parentPath) {
    this.selectedFiles.forEach(filePath => {
      if (filePath.startsWith(parentPath + '/')) {
        this.selectedFiles.add(filePath);
      }
    });

    this.addChildrenFromTree(this.fileTreeData, parentPath, '');
  }

  deselectAllChildren(parentPath) {
    const toDelete = Array.from(this.selectedFiles).filter(filePath =>
      filePath.startsWith(parentPath + '/')
    );
    toDelete.forEach(filePath => this.selectedFiles.delete(filePath));
  }

  addChildrenFromTree(files, targetPath, currentPath) {
    files.forEach(file => {
      const fullPath = currentPath ? `${currentPath}/${file.name}` : file.name;

      if (fullPath === targetPath && file.children) {
        file.children.forEach(child => {
          const childPath = `${fullPath}/${child.name}`;
          this.selectedFiles.add(childPath);

          if (child.type === 'directory' && child.children) {
            this.addChildrenFromTree([child], childPath, fullPath);
          }
        });
      } else if (file.children) {
        this.addChildrenFromTree(file.children, targetPath, fullPath);
      }
    });
  }

  async handlePopupSubmit() {
    this.showPopupLoading(true);

    const onlyFiles = Array.from(this.selectedFiles)
      .filter(path => this.pathTypeMap.get(path) === 'file');

    if (onlyFiles.length === 0) {
      alert('Please select at least one file.');
      this.showPopupLoading(false);
      return;
    }

    const config = {
      upload_id: this.upload_id,
      selected_files: onlyFiles,
      options: {
        remove_empty_files: document.getElementById('removeEmptyFiles').checked,
        minimize_line_count: document.getElementById('minimizeLineCount').checked
      },
      include_files: this.parseCommaSeparated(document.getElementById('includeFiles').value),
      exclude_files: this.parseCommaSeparated(document.getElementById('excludeFiles').value),
      include_extensions: this.parseCommaSeparated(document.getElementById('includeExtensions').value),
      exclude_extensions: this.parseCommaSeparated(document.getElementById('excludeExtensions').value)
    };

    try {
      const resp = await fetch('/api/process-files', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config)
      });
      if (!resp.ok) throw new Error('Processing failed');

      const blob = await resp.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'processed_document.docx';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

      this.hidePopup();
      alert('Document generated successfully!');
    } catch (err) {
      console.error(err);
      alert('Error processing files. Please try again.');
    } finally {
      this.showPopupLoading(false);
    }
  }

  parseCommaSeparated(value) {
    return value.split(',')
      .map(item => item.trim())
      .filter(item => item.length > 0);
  }

  showLoading(show) {
    const submitText = document.getElementById('submitText');
    const submitLoader = document.getElementById('submitLoader');
    const submitButton = document.querySelector('button[type="submit"]');

    if (show) {
      submitText.classList.add('hidden');
      submitLoader.classList.remove('hidden');
      submitButton.disabled = true;
    } else {
      submitText.classList.remove('hidden');
      submitLoader.classList.add('hidden');
      submitButton.disabled = false;
    }
  }

  showPopupLoading(show) {
    const submitText = document.getElementById('popupSubmitText');
    const submitLoader = document.getElementById('popupSubmitLoader');
    const submitButton = document.getElementById('submitPopup');

    if (show) {
      submitText.classList.add('hidden');
      submitLoader.classList.remove('hidden');
      submitButton.disabled = true;
    } else {
      submitText.classList.remove('hidden');
      submitLoader.classList.add('hidden');
      submitButton.disabled = false;
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new FileProcessor();
});
