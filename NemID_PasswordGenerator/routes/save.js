var express = require('express');
var router = express.Router();

/* POST */
router.post('/', function(req, res, next) {
    const c = JSON.stringify(req.body.cpr);
    const e = req.body.nemId;

    res.json(`${e.substr(0, 2)}${c.substr(c.length - 2)}`);
});

module.exports = router;