var createError = require('http-errors');
var express = require('express');
var logger = require('morgan');

var NemIDCodeGenerator = require('./routes/index');

var app = express();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use('/nemid-auth', NemIDCodeGenerator);

module.exports = app;