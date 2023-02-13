const express = require('express');
const app = express();
const path = require("path");
var bodyParser = require('body-parser');
var spawn = require("child_process").spawn;
app.use(express.static(path.join(__dirname, 'public')));
var msg = ""

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(bodyParser.urlencoded({ extended: true }));

function runPythonScript(url) {
  return new Promise((resolve, reject) => {
    var process = spawn('python', ["./app.py", url]);
    process.stdout.on('data', function(data) {
        var pyOutput = JSON.parse(data.toString());
        resolve(pyOutput);
    });
    process.stderr.on('data', function(error) {
        console.error(error.toString());
        reject(error);
    });
  });
}

app.get("/", function(req, res) {
  res.render("index");
});

app.get("/dangerlink", function(req, res) {
  res.render("riskyLink");
});

app.get("/safelink", function(req, res) {
  res.render("approvedLink");
});

app.get("/careful", function(req, res) {
  res.render("careful", {msg: msg});
});

app.post("/sendurl", async function(req, res) {
  var url = req.body.url;
  try {
    var pyOutput = await runPythonScript(url);
    console.log(typeof(pyOutput));
    console.log(pyOutput);
    if (pyOutput[0] == 1) {
        res.redirect("/dangerlink");
    } else if (pyOutput[0] == 0) {
        res.redirect("/safelink");
    } else if (pyOutput[0] == 2) {
        res.redirect("/careful");
        msg = pyOutput[1]
    } else {
        res.redirect("/");
    }
  } catch (error) {
    console.error(error);
    res.redirect("/");
  }
});


const port = 3000;
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});
