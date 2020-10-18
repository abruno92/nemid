var createError = require('http-errors');
var express = require('express');
var logger = require('morgan');

var PasswordRouter = require('./routes/save');

var app = express();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use('/generate-password-nemID', PasswordRouter);

module.exports = app;