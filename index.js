#!/usr/bin/nodejs

// -------------- load packages -------------- //
// INITIALIZATION STUFF

var express = require('express');
var bodyParser = require('body-parser');
var app = express();
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json())

var https = require('http');
var hbs = require('hbs');
const { read } = require('fs');
const { REFUSED } = require('dns');

app.set('view engine', 'hbs');
app.use(express.static('static'));

// -------------- express 'get' handlers -------------- //
// These 'getters' are what fetch your pages

app.get('/', function(req, res) {
    res.render('input');
    console.log('input page loaded');
})

app.post('/generate', make_api_request, function(req, res) {
    var obj = res.locals.obj;
    var data = [];
    for(i = 0; i < obj.length; i++) {
        data[i] = {'number': i + 1, 'questions': obj[i]};
        for(j = 0; j < obj[i].length; j++) {
            obj[i][j] = {'number': j+1, 'question': obj[i][j]};
        }
    };
    res.render('output', {'tests': data});
    console.log('This is the main page.');
});

function make_api_request(req, res, next) {
    var url = 'http://127.0.0.1:5000/tests/get_test';

    var arr = req.body.questionsText.split('\n');
    var newArr = [];
    for(i = 0; i < arr.length; i += 2) {
        newArr[newArr.length] = arr[i].replace('\r', '');
    }
    console.log(arr);
    console.log(newArr);
    var options =  { headers : {
            'User-Agent': 'request'
        },
        'tests': req.body.numTests,
        'questions': newArr
    }

    https.get(url, options, function(response) {
        var rawData = '';
        response.on('data', function(chunk) {
            rawData += chunk;
        });

        response.on('end', function() {
            obj = JSON.parse(rawData);
            res.locals.obj = obj;
            next();
        });

    }).on('error', function(e) {
        console.error(e);
    });
}

// -------------- listener -------------- //
// // The listener is what keeps node 'alive.'

var listener = app.listen(process.env.PORT || 80, process.env.HOST || "0.0.0.0", function() {
    console.log("Express server started");
});
