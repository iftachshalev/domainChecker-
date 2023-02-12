const express = require('express');
const app = express();
const path = require("path");
var bodyParser = require('body-parser');
var spawn = require("child_process").spawn;
app.use(express.static(path.join(__dirname, 'public')));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(bodyParser.urlencoded({ extended: true }));

app.get("/", function(req, res) {
  res.render("index");
});

app.post("/sendurl", function(req, res) {
  var url = req.body.url;
  runPythonScript(url);
  res.redirect("/");
});
  
function runPythonScript(url) {
  var process = spawn('python', ["./app.py", url]);
  process.stdout.on('data', function(data) {
      var pyOutput = JSON.parse(data.toString());
      console.log(pyOutput[0]);
  });
  process.stderr.on('data', function(error) {
      console.error(error.toString());
  });
}

const port = 3000;
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});
