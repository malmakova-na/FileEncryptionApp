const {contextBridge, ipcRenderer} = require('electron');
const path = require('path');

ipcRenderer.on('showPage', (e, isRegistrate) => {
  if(!isRegistrate) {
    ipcRenderer.send('redirect', path.join(__dirname, `/src/pages/singIn.html`));
  }
})

contextBridge.exposeInMainWorld('clickFunctions', {
  chooseAnyFile: () => ipcRenderer.invoke("clickFunctions"),
  chooseFilterFile: () => ipcRenderer.invoke("decriptFiles"),
  redirect: () => ipcRenderer.invoke("registrate"),
  registrate: () =>  ipcRenderer.send('redirect', path.join(__dirname, `/src/pages/build.html`)),
  encrypt: (path) => ipcRenderer.send("encrypt", path),
  decrypt: (path) => ipcRenderer.send("decrypt", path),
  onMessage: callback => listener = callback
})
ipcRenderer.on('replyResponse', (event, msg)=>{
  if (listener) {
    listener(msg);
 } else {
    console.warn('No listener');
 }
})
