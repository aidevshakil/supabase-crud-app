const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const uploadStatus = document.getElementById('uploadStatus');
const filesList = document.getElementById('filesList');
const refreshBtn = document.getElementById('refreshBtn');

const editModal = document.getElementById('editModal');
const newFileNameInput = document.getElementById('newFileName');
const editRecordIdInput = document.getElementById('editRecordId');
const cancelEditBtn = document.getElementById('cancelEditBtn');
const saveEditBtn = document.getElementById('saveEditBtn');

// Load files on start
document.addEventListener('DOMContentLoaded', fetchFiles);
refreshBtn.addEventListener('click', fetchFiles);

// Drag & Drop Handlers
dropzone.addEventListener('click', () => fileInput.click());

dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('dragover');
});

dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
        handleFileUpload(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length) {
        handleFileUpload(fileInput.files[0]);
    }
});

async function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('file', file);

    uploadStatus.textContent = 'Uploading...';
    uploadStatus.className = 'status-msg';

    try {
        const res = await fetch('/api/files', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        if (res.ok) {
            uploadStatus.textContent = 'Upload successful!';
            uploadStatus.className = 'status-msg success';
            fetchFiles(); // Refresh list
        } else {
            uploadStatus.textContent = 'Upload failed: ' + (data.detail || 'Unknown error');
            uploadStatus.className = 'status-msg error';
        }
    } catch (err) {
        uploadStatus.textContent = 'Error: ' + err.message;
        uploadStatus.className = 'status-msg error';
    }

    // Reset input
    fileInput.value = '';
    setTimeout(() => { uploadStatus.textContent = ''; }, 5000);
}

async function fetchFiles() {
    filesList.innerHTML = '<tr><td colspan="4" style="text-align:center;">Loading...</td></tr>';
    refreshBtn.style.transform = 'rotate(180deg)';
    
    try {
        const res = await fetch('/api/files');
        const data = await res.json();
        
        filesList.innerHTML = '';
        if (data.success && data.data.length > 0) {
            data.data.forEach(file => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${file.filename}</td>
                    <td>${file.file_size}</td>
                    <td>${file.content_type}</td>
                    <td class="actions-cell">
                        <button class="btn-action" onclick="downloadFile('${file.filename}')">DL</button>
                        <button class="btn-action" onclick="openEditModal('${file.id}', '${file.filename}')">Edit</button>
                        <button class="btn-action btn-delete" onclick="deleteFile('${file.filename}')">Del</button>
                    </td>
                `;
                filesList.appendChild(tr);
            });
        } else {
            filesList.innerHTML = '<tr><td colspan="4" style="text-align:center;">No files found.</td></tr>';
        }
    } catch (err) {
        filesList.innerHTML = `<tr><td colspan="4" class="error" style="text-align:center;">Failed to load files: ${err.message}</td></tr>`;
    }

    setTimeout(() => { refreshBtn.style.transform = 'rotate(0deg)'; }, 300);
}

async function downloadFile(filename) {
    window.location.href = `/api/files/${encodeURIComponent(filename)}/download`;
}

async function deleteFile(filename) {
    if (!confirm(`Are you sure you want to delete ${filename}?`)) return;
    
    try {
        const res = await fetch(`/api/files/${encodeURIComponent(filename)}`, { method: 'DELETE' });
        if (res.ok) {
            fetchFiles();
        } else {
            const data = await res.json();
            alert('Delete failed: ' + data.detail);
        }
    } catch (err) {
        alert('Error: ' + err.message);
    }
}

// Modal Handlers
function openEditModal(id, currentName) {
    editRecordIdInput.value = id;
    newFileNameInput.value = currentName;
    editModal.classList.add('show');
}

function closeEditModal() {
    editModal.classList.remove('show');
}

cancelEditBtn.addEventListener('click', closeEditModal);

saveEditBtn.addEventListener('click', async () => {
    const id = editRecordIdInput.value;
    const newName = newFileNameInput.value;
    
    if (!newName) return alert('Filename cannot be empty');
    
    // API endpoint expects PUT /api/files/{id}?new_filename=...
    try {
        const res = await fetch(`/api/files/${encodeURIComponent(id)}?new_filename=${encodeURIComponent(newName)}`, {
            method: 'PUT'
        });
        
        if (res.ok) {
            closeEditModal();
            fetchFiles();
        } else {
            const data = await res.json();
            alert('Update failed: ' + data.detail);
        }
    } catch (err) {
        alert('Error: ' + err.message);
    }
});
