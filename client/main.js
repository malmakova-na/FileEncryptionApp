const { app, BrowserWindow, dialog, ipcMain, ipcRenderer } = require('electron')
const path = require('path');
const fetch = require('electron-fetch').default
const fs = require('fs');
const { exec, spawn } = require('child_process');
const { URL } = require('url');

let mainWindow

async function sh(cmd) {
  return new Promise(function (resolve, reject) {
    exec(cmd, (err, stdout, stderr) => {
      if (err) {
        reject(err);
      } else {
        resolve({ stdout, stderr });
      }
    });
  });
}

async function getRequest(adress, params, method ) {
  let url = new URL(`http://127.0.0.1:6005/${adress}`);
  Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
  const response = await fetch(url, {
    method: method
  });
  return response;
}

async function getAes() {
  const dir = path.join(__dirname, `/src/userFiles/id`);
  const id = fs.readFileSync(dir, 'utf-8');
  const params = {"id":id};
  const response = await getRequest("get_aes", params, "GET");
  
  return response;

}

async function createFiles() {
  let { stdout } = await sh('python3 python_scripts/generate_rsa_keys.py src/userFiles');
  for (let line of stdout.split('\n')) {
    console.log(`> ${line}`);
  }
  const key_pub = fs.readFileSync(path.join(__dirname, `src/userFiles/key.pub`), 'utf-8');

  const params = {"pub_key":key_pub}; 
  const response = await getRequest ("registration", params, 'POST')

  const answ = await response.json();
  const id =  answ.id;

  fs.writeFileSync('src/userFiles/id', id);

}

function isExist(fileName) {
  return fs.existsSync(path.join(__dirname, `/src/userFiles/${fileName}`));
}
async function checkFiles() {
  const isFind = isExist('key') && isExist('key.pub') && isExist('id');
  if(isFind){
    const response = await getAes();
    const isValidUser = await response.status === 200 ? true : false;
    mainWindow.send('showPage', isFind && isValidUser); 
  } else {
    mainWindow.send('showPage', isFind); 
  }
}

 function createUserFiles () {
  const dir = path.join(__dirname, `/src/userFiles`);
  if(!fs.existsSync(dir)){
    fs.mkdirSync(dir);
  }
  createFiles();
}

function createWindow () {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      enableRemoteModule: true,
      nodeIntegration: true,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    }
  })
  ipcMain.handle('clickFunctions', (event) => {
    return dialog.showOpenDialog({properties: ['openFile']});
  })
  ipcMain.handle('decriptFiles', (event) => {
    return dialog.showOpenDialog({properties: ['openFile'], 
      filters: [{name:"encrypt files", extensions: ['encrypt']}]
    });
  })

  ipcMain.on('encrypt', async (event, filePath) => {
    const response = await getAes();
    const answ = await response.json();
    const AES = BigInt(answ.aes_key).toString();
    let {stdout} = spawn("python3", ["python_scripts/aes_cript.py", "encrypt", AES, "src/userFiles/key", filePath]);
    
    stdout.on("data", function (data) {
        process.stdout.write(data.toString())
        event.reply('replyResponse', data.toString());
    })
  
  })

  ipcMain.on('decrypt', async (event, filePath) => {
    const response = await getAes();
    const answ = await response.json();
    const AES = BigInt(answ.aes_key).toString();
    let {stdout} = spawn("python3", ["python_scripts/aes_cript.py", "decrypt", AES, "src/userFiles/key", filePath]);

    stdout.on("data", function (data) {
      process.stdout.write(data.toString())
      event.reply('replyResponse', data.toString());
  })
  })

  ipcMain.handle('registrate',  (event) => {
    createUserFiles()
  })

  ipcMain.on('redirect', (event, page) => {
    console.log(page)
    mainWindow.loadFile(page);
  })

  mainWindow.loadFile(path.join(__dirname, `/src/pages/build.html`))

  //mainWindow.webContents.openDevTools()
}


app.whenReady().then(() => {
  createWindow()

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
  checkFiles()
})


app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

