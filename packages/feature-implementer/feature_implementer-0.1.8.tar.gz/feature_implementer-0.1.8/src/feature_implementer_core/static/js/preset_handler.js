/**
 * Handles preset management functionality
 */
document.addEventListener('DOMContentLoaded', function() {
    const addPresetButton = document.getElementById('add-preset-button');
    const addPresetModal = document.getElementById('add-preset-modal');
    const modalOverlay = document.getElementById('modal-overlay');
    const savePresetButton = document.getElementById('save-preset-button');
    
    // Show/hide "Save as Preset" button based on selected files
    function updateAddPresetButtonVisibility() {
        const selectedFiles = getSelectedFiles();
        if (addPresetButton) {
            addPresetButton.style.display = selectedFiles.length > 0 ? 'block' : 'none';
        }
    }
    
    // Initialize "Save as Preset" button visibility
    updateAddPresetButtonVisibility();
    
    // Listen for changes in the selected files list
    document.addEventListener('selectedFilesChanged', function() {
        updateAddPresetButtonVisibility();
    });
    
    // Add preset button functionality
    if (addPresetButton) {
        addPresetButton.addEventListener('click', function() {
            showAddPresetModal();
        });
    }
    
    // Save preset button functionality
    if (savePresetButton) {
        savePresetButton.addEventListener('click', function() {
            savePreset();
        });
    }
    
    // Refresh presets from server on page load
    console.log("Refreshing presets on page load");
    refreshPresets().then(() => {
        console.log("Initial preset refresh complete");
        // Initialize preset selector with checkboxes and counter
        initPresetSelector();
    }).catch(() => {
        console.log("Initial preset refresh failed, initializing with existing data");
        // Initialize anyway even if refresh fails
        initPresetSelector();
    });
    
    /**
     * Shows the add preset modal with currently selected files
     */
    function showAddPresetModal() {
        // Get all selected files
        const selectedFiles = getSelectedFiles();
        if (selectedFiles.length === 0) {
            console.warn('No files selected when trying to create preset');
            return;
        }
        
        // Show the modal using the centralized function
        showModal('add-preset-modal');
        
        // Clear any previous errors
        document.getElementById('preset-error').style.display = 'none';
        document.getElementById('preset-error').textContent = '';
        
        // Clear the input field
        document.getElementById('preset-name').value = '';
        
        // Populate the files summary
        const filesSummaryEl = document.getElementById('preset-files-summary');
        let filesHtml = '<p>Selected files:</p><ul class="preset-file-list">';
        
        selectedFiles.forEach(file => {
            const displayName = file.filename || 
                               (typeof file.path === 'string' ? file.path.split('/').pop() : 'Unknown file');
            filesHtml += `<li>${displayName}</li>`;
        });
        
        filesHtml += '</ul>';
        filesSummaryEl.innerHTML = filesHtml;
    }
});

/**
 * Closes the add preset modal
 */
function closeAddPresetModal() {
    closeModal('add-preset-modal');
}

/**
 * Saves the current selected files as a preset
 */
function savePreset() {
    const presetName = document.getElementById('preset-name').value.trim();
    const errorEl = document.getElementById('preset-error');
    
    errorEl.style.display = 'none'; // Reset error state
    
    if (!presetName) {
        errorEl.textContent = 'Please enter a preset name';
        errorEl.style.display = 'block';
        return;
    }
    
    const selectedFiles = getSelectedFiles();
    if (selectedFiles.length === 0) {
        errorEl.textContent = 'No files selected';
        errorEl.style.display = 'block';
        return;
    }
    
    // Extract just the paths as strings and validate
    const filePaths = [];
    for (const file of selectedFiles) {
        if (!file || !file.path) {
            console.warn('Invalid file object in selection:', file);
            continue;
        }
        // Ensure it's a string
        filePaths.push(String(file.path));
    }
    
    if (filePaths.length === 0) {
        errorEl.textContent = 'No valid file paths in selection';
        errorEl.style.display = 'block';
        return;
    }
    
    // Create payload
    const payload = {
        name: presetName,
        files: filePaths
    };
    
    // Debug
    console.log('Sending preset data:', JSON.stringify(payload));
    
    // Show loading state
    const saveButton = document.getElementById('save-preset-button');
    if (saveButton) {
        saveButton.disabled = true;
        saveButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
    }
    
    // Send the request to the server
    fetch('/presets', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        // Reset button state
        if (saveButton) {
            saveButton.disabled = false;
            saveButton.innerHTML = 'Save Preset';
        }
        
        // Check if response is OK first
        if (!response.ok) {
            return response.text().then(text => {
                console.error('Error response:', response.status, response.statusText);
                console.error('Response content:', text.substring(0, 500));
                
                // Try to parse as JSON if possible
                try {
                    const json = JSON.parse(text);
                    throw new Error(json.error || 'Server error');
                } catch (e) {
                    // If not JSON, show relevant part of the HTML error
                    if (text.includes('<!doctype')) {
                        throw new Error('Server error: Received HTML instead of JSON');
                    }
                    throw new Error(`Server error: ${text.substring(0, 100)}`);
                }
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            // Handle error
            errorEl.textContent = data.error;
            errorEl.style.display = 'block';
        } else {
            // Format the presets to match our expected structure
            const formattedPresets = {};
            if (data.presets) {
                for (const [name, files] of Object.entries(data.presets)) {
                    formattedPresets[name] = { files: files };
                }
            }
            
            // Success - refresh presets
            updatePresets(formattedPresets);
            closeAddPresetModal();
        }
    })
    .catch(error => {
        console.error('Preset save error:', error);
        errorEl.textContent = `Error saving preset: ${error.message}`;
        errorEl.style.display = 'block';
    });
}

/**
 * Updates the preset selection counter display
 */
function updatePresetSelectionCounter() {
    const selectedPresets = document.querySelectorAll('input[name="presets"]:checked');
    const presetTitle = document.querySelector('.preset-selector .section-title');
    
    if (!presetTitle) return;
    
    // Remove existing counter if present
    const existingCounter = presetTitle.querySelector('.preset-selected-count');
    if (existingCounter) {
        existingCounter.remove();
    }
    
    // Add counter if presets are selected
    if (selectedPresets.length > 0) {
        const counter = document.createElement('span');
        counter.className = 'preset-selected-count';
        counter.textContent = selectedPresets.length;
        presetTitle.appendChild(counter);
    }
}

/**
 * Refreshes the presets data from the server
 * @returns {Promise} Promise that resolves when presets are refreshed
 */
function refreshPresets() {
    console.log("Refreshing presets from server");
    return fetch('/presets', {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server responded with status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            console.error("Error refreshing presets:", data.error);
        } else {
            // Format the presets to match our expected structure
            const formattedPresets = {};
            if (data.presets) {
                for (const [name, files] of Object.entries(data.presets)) {
                    formattedPresets[name] = { files: files };
                }
            }
            
            // Update presets in UI and global variable
            window.presets = formattedPresets;
            updatePresets(formattedPresets);
            console.log("Presets refreshed successfully");
        }
        return data;
    })
    .catch(error => {
        console.error("Error refreshing presets:", error);
        throw error;
    });
}

/**
 * Handles multiple preset selections from checkboxes
 * @param {string} presetName - The name of the selected/deselected preset
 * @param {boolean} isChecked - Whether the preset was checked or unchecked
 */
function handleMultiplePresetSelection(presetName, isChecked) {
    console.log("Selected preset:", presetName, "Is checked:", isChecked);
    
    const presetDefinition = window.presets[presetName];
    console.log("Full preset definition from window.presets:", JSON.stringify(presetDefinition));

    if (!presetDefinition || typeof presetDefinition !== 'object') {
        console.warn('Preset definition not found or invalid for:', presetName, 'Refreshing from server...');
        refreshPresets().then(() => {
            handleMultiplePresetSelection(presetName, isChecked); // Try again
        });
        return;
    }

    let rawFileArrayFromPreset;
    if (presetDefinition.files) {
        if (Array.isArray(presetDefinition.files)) {
            console.log("[DEBUG] Preset files structure: { files: ARRAY }");
            rawFileArrayFromPreset = presetDefinition.files;
        } else if (typeof presetDefinition.files === 'object' && presetDefinition.files.files && Array.isArray(presetDefinition.files.files)) {
            console.log("[DEBUG] Preset files structure: { files: { files: ARRAY } } - using inner list.");
            rawFileArrayFromPreset = presetDefinition.files.files;
        } else {
            // Fallback for other unexpected object structures, e.g. { 0: "path1", 1: "path2" }
            // This was the path that could lead to [["path1","path2"]] if presetDefinition.files was { someKey: ["path1","path2"] }
            // For { files: { files: ARRAY } }, this fallback is not ideal as Object.values({files: ARRAY}) is [[ARRAY]].
            // The specific checks above should handle the primary cases.
            console.warn("[DEBUG] presetDefinition.files is an object but not an array or the expected nested structure. Attempting Object.values(). Current presetDefinition.files:", JSON.stringify(presetDefinition.files));
            if (typeof presetDefinition.files === 'object') {
                 rawFileArrayFromPreset = Object.values(presetDefinition.files);
            }
        }
    }
    rawFileArrayFromPreset = rawFileArrayFromPreset || [];
    console.log("[DEBUG] Raw file array from preset before flattening/mapping:", JSON.stringify(rawFileArrayFromPreset));

    // Ensure all values are strings and handle potential nested arrays from Object.values()
    const finalFilePathsArray = rawFileArrayFromPreset.flat().map(file => String(file).trim()).filter(file => file.length > 0);
    console.log("[DEBUG] Final processed file paths from preset:", JSON.stringify(finalFilePathsArray));

    if (finalFilePathsArray.length === 0 && isChecked) {
        console.warn("Preset", presetName, "is selected but contains no valid file paths after processing.");
        // Potentially show a message to the user or uncheck the preset?
        // For now, we'll proceed, and it will likely select no files.
    }
    
    const presetFilePaths = new Set(finalFilePathsArray);
    console.log('[DEBUG] Files in preset (Set):', JSON.stringify(Array.from(presetFilePaths)));
    
    // Get all currently selected presets (for logic involving multiple selections)
    const selectedPresetCheckboxes = document.querySelectorAll('input[name="presets"]:checked');
    
    if (isChecked) {
        let filesChecked = 0; // Ensure declaration

        // If this is the first preset being selected, clear all current selections first
        if (selectedPresetCheckboxes.length === 1 && selectedPresetCheckboxes[0].value === presetName) {
            console.log("First preset selected, clearing all current selections");
            clearSelectedFiles(); // This calls updateSelectedFilesList
            document.querySelectorAll('.file-label.preset-file').forEach(label => {
                label.classList.remove('preset-file');
            });
        }
        
        const allFileCheckboxes = document.querySelectorAll('input[name="context_files"]');
        console.log(`[DEBUG] Number of file checkboxes in DOM: ${allFileCheckboxes.length}`);

        allFileCheckboxes.forEach(checkbox => {
            const filePath = checkbox.value.trim(); // Trim to be safe
            // console.log(`[DEBUG] Processing checkbox file: "${filePath}"`);

            const exactMatch = presetFilePaths.has(filePath);
            // console.log(`[DEBUG] Exact match for "${filePath}" in preset Set: ${exactMatch}`);
            
            let basenameMatch = false;
            if (!exactMatch) {
                const checkboxBasename = filePath.split('/').pop();
                for (const presetPathString of presetFilePaths) { // Iterate over the Set
                    if (typeof presetPathString !== 'string') {
                        console.error(`[DEBUG] Item in presetFilePaths Set is not a string: `, presetPathString);
                        continue;
                    }
                    const presetBasename = presetPathString.split('/').pop();
                    if (checkboxBasename === presetBasename) {
                        basenameMatch = true;
                        console.log(`[DEBUG] Basename match: ${checkboxBasename} (from "${filePath}") with ${presetBasename} (from "${presetPathString}")`);
                        break;
                    }
                }
                // console.log(`[DEBUG] Basename match for "${filePath}": ${basenameMatch}`);
            }

            if (exactMatch || basenameMatch) {
                if (!checkbox.checked) { // Check only if not already checked
                    checkbox.checked = true;
                }
                filesChecked++;
                // console.log(`[DEBUG] Marked as checked: "${filePath}"`);
                
                const fileLabel = checkbox.closest('label');
                if (fileLabel) {
                    fileLabel.classList.add('preset-file');
                }
            } else {
                // If combining presets, we don't uncheck files not in this specific preset here.
                // Unchecking happens when a preset is deselected (in the 'else' branch below)
                // or if clearSelectedFiles() was called.
                // console.log(`[DEBUG] No match for checkbox file: "${filePath}" in preset "${presetName}"`);
            }
        });
        
        console.log(`[SUCCESS] Checked ${filesChecked} files from preset "${presetName}"`);
        
        updateSelectedFilesList(); // Crucial to update the UI
        updatePresetSelectionCounter();
        
        const selectedFilesContainer = document.querySelector('.selected-files-container');
        if (selectedFilesContainer) {
            selectedFilesContainer.style.display = 'block';
        }

    } else { // When unchecking a preset
        let filesUnchecked = 0;
        // ... (rest of the unchecking logic - ensure it also uses finalFilePathsArray for consistency)
        // For brevity, I'm focusing on the 'isChecked' part. The unchecking logic should
        // use 'finalFilePathsArray' (derived from the preset being unchecked) to determine which files
        // were *unique* to this preset and should now be unchecked.

        // Get the files of the preset being unchecked
        const uncheckedPresetFilePaths = new Set(finalFilePathsArray); // Files from the preset being deselected

        // Collect all files from OTHER currently selected presets
        const filesFromOtherSelectedPresets = new Set();
        selectedPresetCheckboxes.forEach(cb => { // selectedPresetCheckboxes are those still checked
            const otherPresetName = cb.value;
            if (otherPresetName === presetName) return; // Skip the one being deselected

            const otherPresetDef = window.presets[otherPresetName];
            if (otherPresetDef && otherPresetDef.files) {
                let otherFilesList;
                if (Array.isArray(otherPresetDef.files)) {
                    otherFilesList = otherPresetDef.files;
                } else if (typeof otherPresetDef.files === 'object' && otherPresetDef.files.files && Array.isArray(otherPresetDef.files.files)) {
                    otherFilesList = otherPresetDef.files.files;
                } else if (typeof otherPresetDef.files === 'object') {
                    otherFilesList = Object.values(otherPresetDef.files);
                }
                otherFilesList = (otherFilesList || []).flat().map(f => String(f).trim()).filter(f => f.length > 0);
                otherFilesList.forEach(f => filesFromOtherSelectedPresets.add(f));
            }
        });
        console.log('[DEBUG] Files from other selected presets:', JSON.stringify(Array.from(filesFromOtherSelectedPresets)));


        const allFileCheckboxes = document.querySelectorAll('input[name="context_files"]');
        allFileCheckboxes.forEach(checkbox => {
            const filePath = checkbox.value.trim();
            let shouldUncheck = false;

            // Was this file part of the preset we just unchecked?
            if (uncheckedPresetFilePaths.has(filePath)) { // Exact match first
                shouldUncheck = true;
            } else { // Try basename match if exact failed
                const checkboxBasename = filePath.split('/').pop();
                for (const uncheckedPresetPath of uncheckedPresetFilePaths) {
                    if (checkboxBasename === String(uncheckedPresetPath).split('/').pop()) {
                        shouldUncheck = true;
                        console.log(`[DEBUG] Unchecking (basename): ${filePath} due to deselection of ${presetName}`);
                        break;
                    }
                }
            }
            
            if (shouldUncheck) {
                // Now, is this file ALSO part of any *other* still-selected preset?
                let inAnotherSelectedPreset = filesFromOtherSelectedPresets.has(filePath);
                if (!inAnotherSelectedPreset) {
                    const checkboxBasename = filePath.split('/').pop();
                     for (const otherSelectedPath of filesFromOtherSelectedPresets) {
                        if (checkboxBasename === String(otherSelectedPath).split('/').pop()) {
                            inAnotherSelectedPreset = true;
                            break;
                        }
                    }
                }

                if (!inAnotherSelectedPreset) {
                    if (checkbox.checked) { // Uncheck only if currently checked
                        checkbox.checked = false;
                        filesUnchecked++;
                    }
                    const fileLabel = checkbox.closest('label');
                    if (fileLabel) {
                        fileLabel.classList.remove('preset-file');
                    }
                }
            }
        });
        console.log(`[SUCCESS] Unchecked ${filesUnchecked} files due to deselection of preset "${presetName}"`);
        
        updateSelectedFilesList();
        updatePresetSelectionCounter();
        // If no files are selected at all after unchecking, the selected-files-container might need to be hidden
        // updateSelectedFilesList() should handle the empty state text.
    }
}

/**
 * Clear all selected files and uncheck all preset checkboxes
 */
function clearAllPresets() {
    // Uncheck all preset checkboxes
    document.querySelectorAll('input[name="presets"]').forEach(checkbox => {
        checkbox.checked = false;
    });
    
    // Remove visual highlighting from all file labels
    document.querySelectorAll('.file-label.preset-file').forEach(label => {
        label.classList.remove('preset-file');
    });
    
    // Clear all selected files
    clearSelectedFiles();
    
    // Update counter
    updatePresetSelectionCounter();
}

/**
 * Handles preset selection from the radio buttons
 * @param {string} presetName - The name of the selected preset
 */
function handlePresetSelection(presetName) {
    if (!presetName) {
        // "None" selected - clear selections
        clearSelectedFiles();
        
        // Remove all visual highlighting
        document.querySelectorAll('.file-label.preset-file').forEach(label => {
            label.classList.remove('preset-file');
        });
        
        return;
    }
    
    console.log("Selected preset (radio):", presetName);
    console.log("Preset data:", window.presets[presetName]);
    
    const preset = window.presets[presetName];
    if (!preset) {
        console.warn('Preset not found:', presetName);
        return;
    }
    
    // Get the files array from the preset
    // Handle both formats: {files: [...]} and {files: {0: "file1", 1: "file2"}}
    let presetFiles = preset.files || [];
    
    // Check if preset.files is an object but not an array
    if (preset.files && typeof preset.files === 'object' && !Array.isArray(preset.files)) {
        // Convert object to array
        presetFiles = Object.values(preset.files);
    }
    
    // Ensure we have an array to work with
    if (!Array.isArray(presetFiles)) {
        console.warn('Invalid preset files format:', presetName, presetFiles);
        return;
    }
    
    // Ensure all values in the array are strings
    presetFiles = presetFiles.map(file => String(file));
    
    // Clear existing selections
    clearSelectedFiles();
    
    // Remove all visual highlighting first
    document.querySelectorAll('.file-label.preset-file').forEach(label => {
        label.classList.remove('preset-file');
    });
    
    // Select all files from the preset
    const allFileCheckboxes = document.querySelectorAll('input[name="context_files"]');
    
    allFileCheckboxes.forEach(checkbox => {
        const filePath = checkbox.value;
        
        // Check for exact match
        const exactMatch = presetFiles.includes(filePath);
        
        // Check for basename match with absolute paths
        const isAbsolutePathMatch = presetFiles.some(presetPath => {
            // If preset path is absolute and ends with the file path
            if (presetPath.startsWith('/') && filePath.includes('/')) {
                const checkboxBasename = filePath.split('/').pop();
                const presetBasename = presetPath.split('/').pop();
                return checkboxBasename === presetBasename && 
                      (presetPath.endsWith(filePath) || filePath.endsWith(presetPath));
            }
            return false;
        });
        
        if (exactMatch || isAbsolutePathMatch) {
            checkbox.checked = true;
            
            // Add visual highlight
            const fileLabel = checkbox.closest('label');
            if (fileLabel) {
                fileLabel.classList.add('preset-file');
            }
        }
    });
    
    // Update the UI
    updateSelectedFilesList();
}

/**
 * Deletes a preset
 * @param {string} presetName - The name of the preset to delete
 */
function deletePreset(presetName) {
    if (!confirm(`Are you sure you want to delete the preset "${presetName}"?`)) {
        return;
    }
    
    
    fetch(`/presets/${encodeURIComponent(presetName)}`, {
        method: 'DELETE',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server responded with status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            console.error("Preset deletion error:", data.error);
        } else {
            // Format the presets to match our expected structure
            const formattedPresets = {};
            if (data.presets) {
                for (const [name, files] of Object.entries(data.presets)) {
                    formattedPresets[name] = { files: files };
                }
            }
            
            // Update presets in UI and global variable
            window.presets = formattedPresets;
            updatePresets(formattedPresets);
            
            // If preset radio buttons exist, select "None"
            const noneOption = document.querySelector('input[name="preset"][value=""]');
            if (noneOption) {
                noneOption.checked = true;
            }
        }
    })
    .catch(error => {
        console.error("Error deleting preset:", error);
    });
}

/**
 * Updates the presets in the UI
 * @param {Object} presets - The updated presets object
 */
function updatePresets(presets) {
    // Update the global presets object
    window.presets = presets;
    
    // Update the preset selector
    const presetContainer = document.querySelector('.preset-options');
    if (!presetContainer) return;
    
    // Add the 'Clear All' button
    let html = `
        <label class="preset-option">
            <input type="button" id="clear-presets-button" class="button button-small button-secondary" value="Clear All">
        </label>
    `;
    
    // Add all presets as checkboxes
    for (const [name, _] of Object.entries(presets)) {
        html += `
            <label class="preset-option">
                <input type="checkbox" name="presets" value="${name}"> ${name}
                <button type="button" class="action-button" data-preset="${name}" title="Delete preset" onclick="deletePreset('${name}')">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </label>
        `;
    }
    
    presetContainer.innerHTML = html;
    
    
    // Add click handler for clear all button
    const clearButton = document.getElementById('clear-presets-button');
    if (clearButton) {
        clearButton.addEventListener('click', clearAllPresets);
    }
    
    // Reinitialize the preset selector
    initPresetSelector();
}

/**
 * Test function to diagnose JSON issues - called from the console
 */
function testJsonEndpoint() {
    const testData = {
        test: "Testing JSON endpoint",
        timestamp: new Date().toISOString()
    };
    
    console.log("Sending test data:", testData);
    
    fetch('/debug/test-json', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(testData)
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                console.error("Response not OK:", response.status, response.statusText);
                try {
                    return JSON.parse(text);
                } catch (e) {
                    console.error("Failed to parse response as JSON:", text.substring(0, 500));
                    throw new Error(`Non-JSON response: ${text.substring(0, 100)}`);
                }
            });
        }
        return response.json();
    })
    .then(data => {
        console.log("Test JSON endpoint response:", data);
        return data;
    })
    .catch(error => {
        console.error("Error testing JSON endpoint:", error);
    });
}

/**
 * Initializes the preset selector checkboxes with event listeners
 */
function initPresetSelector() {
    const presetCheckboxes = document.querySelectorAll('input[name="presets"]');
    presetCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            handleMultiplePresetSelection(this.value, this.checked);
        });
    });
    
    // Initialize clear button
    const clearButton = document.getElementById('clear-presets-button');
    if (clearButton) {
        clearButton.addEventListener('click', clearAllPresets);
    }
    
    // Initialize counter
    updatePresetSelectionCounter();
}

/**
 * Checks if the currently selected files match any preset and updates
 * preset checkboxes accordingly
 */
function updatePresetCheckboxes() {
    // Get all selected files
    const selectedFiles = getSelectedFiles();
    const selectedFilePaths = new Set(selectedFiles.map(file => file.path));
    
    // Get all preset checkboxes
    const presetCheckboxes = document.querySelectorAll('input[name="presets"]:checked');
    
    // For each checked preset, verify if all its files are still selected
    presetCheckboxes.forEach(checkbox => {
        const presetName = checkbox.value;
        const preset = window.presets[presetName];
        
        if (!preset || !preset.files) return;
        
        // Get the files array from the preset
        let presetFiles = preset.files;
        if (typeof presetFiles === 'object' && !Array.isArray(presetFiles)) {
            presetFiles = Object.values(presetFiles);
        }
        
        // Check if any file from this preset was removed
        const anyFileRemoved = presetFiles.some(presetFile => {
            // Convert to string if needed
            presetFile = String(presetFile);
            
            // Check if this file is not in the selected files
            // First try exact match
            if (selectedFilePaths.has(presetFile)) {
                return false;
            }
            
            // Then try basename match for absolute paths
            const fileBasename = presetFile.split('/').pop();
            const matchedByBasename = Array.from(selectedFilePaths).some(selectedPath => {
                const selectedBasename = selectedPath.split('/').pop();
                return fileBasename === selectedBasename &&
                      (presetFile.endsWith(selectedPath) || selectedPath.endsWith(presetFile));
            });
            
            return !matchedByBasename;
        });
        
        // If any file was removed, uncheck this preset
        if (anyFileRemoved) {
            console.log(`Files from preset "${presetName}" were removed, unchecking preset`);
            checkbox.checked = false;
            
            // Remove visual highlighting from files that are no longer in any selected preset
            updateFileHighlighting();
        }
    });
    
    // Update counter
    updatePresetSelectionCounter();
}

/**
 * Updates visual highlighting for files based on selected presets
 */
function updateFileHighlighting() {
    // First, remove all preset highlighting
    document.querySelectorAll('.file-label.preset-file').forEach(label => {
        label.classList.remove('preset-file');
    });
    
    // Get all selected presets
    const selectedPresets = document.querySelectorAll('input[name="presets"]:checked');
    if (selectedPresets.length === 0) return;
    
    // Get all files from selected presets
    const presetFiles = new Set();
    selectedPresets.forEach(checkbox => {
        const preset = window.presets[checkbox.value];
        if (!preset || !preset.files) return;
        
        let files = preset.files;
        if (typeof files === 'object' && !Array.isArray(files)) {
            files = Object.values(files);
        }
        
        if (Array.isArray(files)) {
            files.forEach(file => presetFiles.add(String(file)));
        }
    });
    
    // Highlight all files that are in selected presets
    const allFileCheckboxes = document.querySelectorAll('input[name="context_files"]');
    allFileCheckboxes.forEach(checkbox => {
        if (!checkbox.checked) return;
        
        const filePath = checkbox.value;
        
        // Check if this file is in any selected preset
        const exactMatch = presetFiles.has(filePath);
        
        // Check for basename match
        const isInPreset = exactMatch || Array.from(presetFiles).some(presetPath => {
            if (presetPath.startsWith('/') && filePath.includes('/')) {
                const checkboxBasename = filePath.split('/').pop();
                const presetBasename = presetPath.split('/').pop();
                return checkboxBasename === presetBasename && 
                      (presetPath.endsWith(filePath) || filePath.endsWith(presetPath));
            }
            return false;
        });
        
        // If this file is in a selected preset, highlight it
        if (isInPreset) {
            const fileLabel = checkbox.closest('label');
            if (fileLabel) {
                fileLabel.classList.add('preset-file');
            }
        }
    });
}

// Make functions globally available
window.handleMultiplePresetSelection = handleMultiplePresetSelection;
window.clearAllPresets = clearAllPresets;
window.initPresetSelector = initPresetSelector;
window.testJsonEndpoint = testJsonEndpoint;
window.refreshPresets = refreshPresets;
window.updatePresetCheckboxes = updatePresetCheckboxes;

// Ensure presets object exists
if (!window.presets) {
    window.presets = {};
}