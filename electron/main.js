const { app, BrowserWindow, session } = require("electron");
const path = require("path");
const { spawn } = require("child_process");

const createWindow = () => {
  const win = new BrowserWindow({
    width: 1200,
    height: 1000,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, "preload.js"),
    },
  });

  session.defaultSession.setPermissionRequestHandler(
    (webContents, permission, callback) => {
      if (permission === "geolocation") {
        callback(true);
      } else {
        callback(false);
      }
    }
  );
  console.log(path.join(__dirname, "frontend/build/index.html"));
  win.loadFile(path.join(__dirname, "frontend/build/index.html"));

  const pythonScript = path.join(__dirname, "backend", "app.py");

  pythonProcess = spawn("python", [pythonScript]);

  pythonProcess.stdout.on("data", (data) => {
    console.log(`Python: ${data}`);
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`Python error: ${data}`);
  });

  pythonProcess.on("close", (code) => {
    console.log(`Python process exited with code ${code}`);
  });

  // Open DevTools only in dev
  // win.webContents.openDevTools();
};

// const startPython = () => {
//   // const scriptPath = path.join(__dirname, "../backend/server.py");
//   // const python = process.platform === "win32" ? "python" : "python3";

//   // pythonProcess = spawn(python, [scriptPath], {
//   //   cwd: path.join(__dirname, "../backend"),
//   // });

//   // const isDev = require("electron-is-dev");
//   // const backendPath = isDev
//   // ? path.join(__dirname, "../backend/server.py")
//   // : path.join(process.resourcesPath, "backend", "server.py");
//   const backendPath = path.join(process.resourcesPath, "backend", "server.py");

//   // const pythonExe = isDev
//   // ? "../backend/venv/Scripts/python.exe"
//   // : path.join(
//   //   process.resourcesPath,
//   //   "backend",
//   //   "venv",
//   //   "Scripts",
//   //   "python.exe"
//   // );
//   const pythonExe = path.join(
//     process.resourcesPath,
//     "backend",
//     "venv",
//     "Scripts",
//     "python.exe"
//   );

//   const pythonProcess = spawn(pythonExe, [backendPath], {
//     cwd: path.dirname(backendPath),
//   });

//   pythonProcess.stdout.on("data", (data) => {
//     console.log(`PYTHON: ${data}`);
//   });

//   pythonProcess.stderr.on("data", (data) => {
//     console.error(`PYTHON ERROR: ${data}`);
//   });

//   pythonProcess.on("close", (code) => {
//     console.log(`Python process exited with code ${code}`);
//   });
// };

// app.whenReady().then(() => {
//   startPython();
//   createWindow();

//   app.on("activate", () => {
//     if (BrowserWindow.getAllWindows().length === 0) createWindow();
//   });
// });

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (pythonProcess) pythonProcess.kill();
  if (process.platform !== "darwin") app.quit();
});
