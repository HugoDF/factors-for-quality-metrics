const stats = require('simple-statistics');
const data = require('../data/buildsForPrComments');

const results = Object.keys(data)
    .reduce( function(prev, key) {
        const curr = data[key];

        const [ number = key, total = 0, fail = 0 ] = curr;

        if(fail > 0 && total > 0 && fail < total){
            prev[key] = fail / total;
        }
        return prev
    }, {});

const sizes = Object.keys(results);
const failureRate = Object.values(results);

const correlation = stats.sampleCorrelation(sizes, failureRate);

// console.log(correlation);
console.log(JSON.stringify([ sizes.map(Number), failureRate ]));
