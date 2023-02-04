const express = require('express');
const app = express();
const path = require("path");
app.use(express.static(path.join(__dirname, 'public')));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.get("/", function(req, res) {
  res.render("index");
});

const port = 3000;
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});
