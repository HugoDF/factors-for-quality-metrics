const stats = require('simple-statistics');
const data = require('../data/volumeOfTestForPrComments');

const results = Object.keys(data)
    .reduce( function(prev, key) {
        const curr = data[key];

        const testRate = curr;

        // if(aggregateFailureRate !== 0) {
        prev[key] = testRate;
        // }

        return prev;
    }, {});

const sizes = Object.keys(results);
const testRate = Object.values(results);

const correlation = stats.sampleCorrelation(sizes, testRate);

console.log(correlation);
// console.log(JSON.stringify([ sizes.map(Number), testRate ]));
