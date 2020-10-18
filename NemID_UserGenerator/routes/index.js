var express = require('express');
var router = express.Router();

/* POST */
router.post('/', function(req, res, next) {
    const c = JSON.stringify(req.body.cpr);
    const e = req.body.email;

    const num = Math.floor(Math.random() * 90000) + 10000;

    res.status(201);
    res.json(`${num}-${c.substr(c.length - 4)}`);
});

module.exports = router;