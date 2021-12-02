const { exec, spawn } = require('child_process');
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
function console_out(out) {
  out.on("data", function (data) {
    process.stdout.write(data.toString())
  })
}
//spawn("python3", ["test_exec.py"], {stdio: "inherit"});
//let child = spawn("python3", ["test_exec.py"])
let cmd = spawn("python3", ["test_exec.py"]);

console_out(cmd.stdout)