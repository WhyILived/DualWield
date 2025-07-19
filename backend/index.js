const { app, BrowserWindow, screen, globalShortcut, ipcMain } = require('electron');
const path = require('path');

console.log('🎬 Starting HT6ix AI Teaching Bot...');
console.log(`📅 Date: ${new Date().toISOString()}`);
console.log(`🖥️  Platform: ${process.platform}`);
console.log(`⚡ Electron version: ${process.versions.electron}`);
console.log(`🟢 Node version: ${process.versions.node}`);

let mainWindow;

function createWindow () {
  console.log('🚀 Creating Electron window...');
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;
  console.log(`📐 Screen dimensions: ${width}x${height}`);

  const win = new BrowserWindow({
    width,
    height,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    skipTaskbar: true,
    focusable: false,
    clickThrough: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  console.log('🌐 Loading frontend HTML...');
  win.loadFile('frontend/index.html');
  
  // Make global for other services
  global.mainWindow = win;

  // Register global shortcuts
  console.log('⌨️  Registering global shortcuts...');
  try {
    const toggleSuccess = globalShortcut.register('/', () => {
      console.log('🎬 Slash key pressed - toggling view');
      win.webContents.send('toggle-view-mode');
    });

    if (toggleSuccess) {
      console.log('✅ Toggle shortcut (/) registered successfully');
    } else {
      console.error('❌ Failed to register toggle shortcut (/)');
    }

    // Register P key for audio visualizer toggle
    const visualizerSuccess = globalShortcut.register('=', () => {
      if (win.isVisible()) {
        console.log('🎵 Toggling audio visualizer focus (= key pressed)');
        win.webContents.send('toggle-visualizer-focus');
      } else {
        console.log('⚠️  Audio visualizer toggle ignored - window not visible');
      }
    });

    if (visualizerSuccess) {
      console.log('✅ Visualizer shortcut (=) registered successfully');
    } else {
      console.error('❌ Failed to register visualizer shortcut (=)');
    }
  } catch (error) {
    console.error('❌ Error registering shortcuts:', error);
  }

  // Set window to ignore mouse events (except for specific areas)
  console.log('🖱️  Setting window to ignore mouse events...');
  win.setIgnoreMouseEvents(true, { forward: true });

  // Add event listeners for debugging
  win.webContents.on('did-finish-load', () => {
    console.log('✅ Frontend loaded successfully');
  });

  win.webContents.on('crashed', () => {
    console.error('💥 Window content crashed!');
  });

  win.on('closed', () => {
    console.log('❌ Window closed');
  });

  win.on('show', () => {
    console.log('👁️  Window shown');
  });

  win.on('hide', () => {
    console.log('👻 Window hidden');
  });

  console.log('✨ Window creation complete');
  return win;
}

// IPC handler for controlling mouse events
ipcMain.handle('set-mouse-events', async (event, enabled, region = null) => {
  console.log(`🖱️ Setting mouse events: ${enabled ? 'enabled' : 'disabled'}`, region ? `for region: ${JSON.stringify(region)}` : '');
  
  try {
    if (enabled && region) {
      global.mainWindow.setIgnoreMouseEvents(false);
      console.log('✅ Mouse events enabled for specific region');
    } else if (enabled) {
      global.mainWindow.setIgnoreMouseEvents(false);
      console.log('✅ Mouse events enabled for entire window');
    } else {
      global.mainWindow.setIgnoreMouseEvents(true, { forward: true });
      console.log('✅ Mouse events disabled (transparent mode)');
    }
    return { success: true };
  } catch (error) {
    console.error('❌ Failed to set mouse events:', error);
    return { success: false, error: error.message };
  }
});

// App event handlers
app.whenReady().then(() => {
  console.log('🚀 App is ready, creating window...');
  mainWindow = createWindow();
  
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      mainWindow = createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  console.log('❌ All windows closed');
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('will-quit', () => {
  console.log('🔄 App will quit, unregistering shortcuts...');
  globalShortcut.unregisterAll();
});

console.log('🎬 HT6ix AI Teaching Bot backend initialized'); 