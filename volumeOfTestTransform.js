const stats = require('simple-statistics');
const data = require('./data/volumeOfTestForTeams');

const results = Object.keys(data)
    .filter( (size) => data[size] && data[size].length > 3)
    .reduce( function(prev, key) {
        const curr = data[key];

        const computeTestRate = curr.map( ([ name, testRate ]) => testRate );

        const sumTestRates = computeTestRate.reduce( (prev, curr) => (prev + curr), 0);

        const numberOfRates = computeTestRate.length;

        const aggregateTestRate = numberOfRates !== 0 ? (sumTestRates / numberOfRates) : 0;

        // if(aggregateFailureRate !== 0) {
        prev[key] = aggregateTestRate;
        // }

        return prev;
    }, {});

const sizes = Object.keys(results);
const testRate = Object.values(results);

const correlation = stats.sampleCorrelation(sizes, testRate);

// console.log(correlation);
console.log(JSON.stringify([ sizes.map(Number), testRate ]));
