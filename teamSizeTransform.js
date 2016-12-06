const stats = require('simple-statistics');
const teamSizes = require('./data/buildInfoForTeams');

const results = Object.keys(teamSizes)
    .filter( (size) => teamSizes[size] && teamSizes[size].length > 3)
    .reduce( function(prev, key) {
        const curr = teamSizes[key];

        const computeFailureRate = curr.map( ([ name, total, fail ]) => {
            return fail / total;
        });

        const sumFailureRates = computeFailureRate.reduce( (prev, curr) => (prev + curr), 0);

        const numberOfRates = computeFailureRate.length;

        const aggregateFailureRate = numberOfRates !== 0 ? (sumFailureRates / numberOfRates) : 0;

        // if(aggregateFailureRate !== 0) {
            prev[key] = aggregateFailureRate;
        // }

        return prev;
    }, {});

const sizes = Object.keys(results);
const failureRate = Object.values(results);

const correlation = stats.sampleCorrelation(sizes, failureRate);

// console.log(correlation);
console.log(JSON.stringify([ sizes.map(Number), failureRate ]));
