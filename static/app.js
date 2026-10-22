// State tracking
let currentVideoInfo = null;
let currentEventSource = null;

document.addEventListener("DOMContentLoaded", () => {
  initSystemStatus();
  initFormListeners();
  refreshDownloadsList();
});

// Check FFmpeg and system environment
async function initSystemStatus() {
  const badge = document.getElementById("system-badge");
  try {
    const res = await fetch("/api/system-status");
    const data = await res.json();
    if (data.ffmpeg_available) {
      badge.className = "system-badge badge-ok";
      badge.innerHTML = '<span class="status-dot"></span> FFmpeg Ready';
    } else {
      badge.className = "system-badge badge-warn";
      badge.innerHTML = '<span class="status-dot"></span> FFmpeg Missing';
      badge.title = "Clipping and format merging require FFmpeg on PATH";
    }
  } catch (e) {
    badge.className = "system-badge badge-warn";
    badge.innerHTML = '<span class="status-dot"></span> Offline';
  }
}

// Wire form, button, and input handlers
function initFormListeners() {
  const urlForm = document.getElementById("url-form");
  const fetchBtn = document.getElementById("fetch-btn");
  const mediaTypeRadios = document.querySelectorAll('input[name="media-type"]');
  const enableClipCheckbox = document.getElementById("enable-clip");
  const downloadBtn = document.getElementById("download-btn");
  const refreshDownloadsBtn = document.getElementById("refresh-downloads-btn");

  urlForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const url = document.getElementById("video-url").value.trim();
    if (!url) return;
    await inspectVideo(url);
  });

  // Switch between Video and Audio format options
  mediaTypeRadios.forEach((radio) => {
    radio.addEventListener("change", (e) => {
      const isAudio = e.target.value === "audio";
      document.getElementById("video-options").classList.toggle("hidden", isAudio);
      document.getElementById("audio-options").classList.toggle("hidden", !isAudio);
    });
  });

  // Enable/disable clipping time inputs
  enableClipCheckbox.addEventListener("change", (e) => {
    const enabled = e.target.checked;
    const clipControls = document.getElementById("clip-controls");
    const startInput = document.getElementById("start-time");
    const endInput = document.getElementById("end-time");

    clipControls.classList.toggle("disabled-area", !enabled);
    startInput.disabled = !enabled;
    endInput.disabled = !enabled;

    if (enabled && !startInput.value) {
      startInput.value = "00:00";
    }
  });

  downloadBtn.addEventListener("click", startDownloadProcess);
  refreshDownloadsBtn.addEventListener("click", refreshDownloadsList);
}

// Inspect YouTube video details
async function inspectVideo(url) {
  const fetchBtn = document.getElementById("fetch-btn");
  const errorBanner = document.getElementById("url-error");
  const configSection = document.getElementById("config-section");

  errorBanner.classList.add("hidden");
  errorBanner.textContent = "";
  fetchBtn.disabled = true;
  fetchBtn.innerHTML = "<span>Inspecting...</span>";

  try {
    const res = await fetch("/api/info", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    const result = await res.json();
    if (!res.ok) {
      throw new Error(result.detail || "Unable to inspect video");
    }

    currentVideoInfo = result.data;
    renderVideoPreview(currentVideoInfo);
    configSection.classList.remove("hidden");
  } catch (err) {
    errorBanner.textContent = err.message;
    errorBanner.classList.remove("hidden");
    configSection.classList.add("hidden");
  } finally {
    fetchBtn.disabled = false;
    fetchBtn.innerHTML = "<span>Inspect Video</span>";
  }
}

// Populate video card and quality choices
function renderVideoPreview(info) {
  document.getElementById("preview-thumbnail").src = info.thumbnail;
  document.getElementById("preview-title").textContent = info.title;
  document.getElementById("preview-author").textContent = info.uploader;
  document.getElementById("preview-duration").textContent = info.duration_formatted;
  document.getElementById("preview-views").textContent = `${Number(info.view_count).toLocaleString()} views`;

  // Populate qualities
  const qualitySelect = document.getElementById("video-quality");
  qualitySelect.innerHTML = '<option value="best">Best Available</option>';

  if (Array.isArray(info.available_resolutions)) {
    info.available_resolutions.forEach((res) => {
      const opt = document.createElement("option");
      opt.value = res;
      opt.textContent = `${res}p`;
      qualitySelect.appendChild(opt);
    });
  }

  // Pre-fill end clipping placeholder with total duration
  if (info.duration > 0) {
    document.getElementById("end-time").placeholder = info.duration_formatted;
  }
}

// Dispatch download request and subscribe to SSE progress
async function startDownloadProcess() {
  if (!currentVideoInfo) return;

  const downloadBtn = document.getElementById("download-btn");
  const progressSection = document.getElementById("progress-section");
  const completionActions = document.getElementById("completion-actions");
  const isAudio = document.querySelector('input[name="media-type"]:checked').value === "audio";
  const isClipEnabled = document.getElementById("enable-clip").checked;

  downloadBtn.disabled = true;
  completionActions.classList.add("hidden");
  progressSection.classList.remove("hidden");
  resetProgressUI();

  const payload = {
    url: currentVideoInfo.webpage_url,
    audio_only: isAudio,
    audio_format: document.getElementById("audio-format").value,
    audio_bitrate: document.getElementById("audio-bitrate").value,
    video_format: document.getElementById("video-container").value,
    video_quality: document.getElementById("video-quality").value,
    start_time: isClipEnabled ? document.getElementById("start-time").value.trim() : null,
    end_time: isClipEnabled ? document.getElementById("end-time").value.trim() : null,
    total_duration: currentVideoInfo.duration,
  };

  try {
    const res = await fetch("/api/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "Download request failed");
    }

    subscribeToProgress(data.job_id);
  } catch (err) {
    alert("Error starting download: " + err.message);
    downloadBtn.disabled = false;
  }
}

// Listen to real-time progress via Server-Sent Events
function subscribeToProgress(jobId) {
  if (currentEventSource) {
    currentEventSource.close();
  }

  const evtSource = new EventSource(`/api/progress/${jobId}/stream`);
  currentEventSource = evtSource;

  evtSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      updateProgressUI(data);

      if (data.status === "completed") {
        evtSource.close();
        handleDownloadComplete(jobId);
      } else if (data.status === "error") {
        evtSource.close();
        handleDownloadError(data.error_message);
      }
    } catch (e) {
      console.error("Failed to parse progress update", e);
    }
  };

  evtSource.onerror = () => {
    console.warn("EventSource disconnected or completed.");
  };
}

function updateProgressUI(data) {
  const fill = document.getElementById("progress-bar-fill");
  const percentText = document.getElementById("progress-percentage");
  const title = document.getElementById("progress-status-title");
  const badge = document.getElementById("progress-status-badge");
  const speed = document.getElementById("stat-speed");
  const eta = document.getElementById("stat-eta");
  const filename = document.getElementById("stat-filename");

  const pct = Math.min(100, Math.max(0, data.percentage || 0));
  fill.style.width = `${pct}%`;
  percentText.textContent = `${pct}%`;

  if (data.status === "downloading") {
    title.textContent = "Downloading stream...";
    badge.textContent = "Downloading";
    badge.className = "badge";
  } else if (data.status === "processing") {
    title.textContent = "Processing and merging streams...";
    badge.textContent = "Processing";
    badge.className = "badge";
  }

  if (data.speed) speed.textContent = data.speed;
  if (data.eta) eta.textContent = data.eta;
  if (data.filename) filename.textContent = data.filename;
}

function resetProgressUI() {
  document.getElementById("progress-bar-fill").style.width = "0%";
  document.getElementById("progress-percentage").textContent = "0%";
  document.getElementById("progress-status-title").textContent = "Preparing job...";
  document.getElementById("progress-status-badge").textContent = "Queued";
  document.getElementById("stat-speed").textContent = "--";
  document.getElementById("stat-eta").textContent = "--";
  document.getElementById("stat-filename").textContent = "Initializing...";
}

function handleDownloadComplete(jobId) {
  const downloadBtn = document.getElementById("download-btn");
  const title = document.getElementById("progress-status-title");
  const badge = document.getElementById("progress-status-badge");
  const completionBox = document.getElementById("completion-actions");
  const link = document.getElementById("browser-download-link");

  title.textContent = "Processing finished successfully!";
  badge.textContent = "Done";
  badge.className = "badge badge-ok";

  const downloadUrl = `/api/download-file/${jobId}`;
  link.href = downloadUrl;
  completionBox.classList.remove("hidden");
  downloadBtn.disabled = false;

  refreshDownloadsList();

  // Automatically initiate browser download prompt
  link.click();
}

function handleDownloadError(msg) {
  const downloadBtn = document.getElementById("download-btn");
  const title = document.getElementById("progress-status-title");
  const badge = document.getElementById("progress-status-badge");

  title.textContent = "Download failed";
  badge.textContent = "Failed";
  badge.className = "badge badge-warn";
  alert("Download error: " + (msg || "Unknown error"));
  downloadBtn.disabled = false;
}

// Fetch list of files in local downloads folder
async function refreshDownloadsList() {
  const container = document.getElementById("downloads-list");
  try {
    const res = await fetch("/api/list-downloads");
    const data = await res.json();
    const files = data.downloads || [];

    if (files.length === 0) {
      container.innerHTML = '<p class="empty-notice">No downloads yet.</p>';
      return;
    }

    container.innerHTML = files
      .map(
        (f) => `
        <div class="download-row">
          <span>${escapeHtml(f.filename)}</span>
          <span class="tag">${f.size_mb} MB</span>
        </div>`
      )
      .join("");
  } catch (err) {
    container.innerHTML = '<p class="empty-notice">Could not load files list.</p>';
  }
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
