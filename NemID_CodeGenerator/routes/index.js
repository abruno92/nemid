var express = require('express');
var router = express.Router();

/* POST */
router.post('/', function(req, res, next) {
    //Check against the data from the database. If it matches this will return a JSON bodywith status code 200. Otherwise it will return a 403(forbidden)

});

module.exports = router;